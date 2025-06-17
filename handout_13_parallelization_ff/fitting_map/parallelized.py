from mpi4py import MPI
import numpy as np
from pathlib import Path
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

from line_profiler import profile
import time

# === Model Function ===
def akimov_phase(phase, A, nu1, m, nu2):
    return A * (np.exp(-nu1 * phase) + m * np.exp(-nu2 * phase)) / (1 + m)

# === Utility Functions ===
def fit_akimov_model(phase, albedo, initial_guess, bounds):
    phase_clean = phase[np.isfinite(phase) & np.isfinite(albedo)]
    albedo_clean = albedo[np.isfinite(phase) & np.isfinite(albedo)]

    if len(phase_clean) < 8 or np.min(phase_clean) > 2:
        return None

    try:
        params, cov = curve_fit(
            akimov_phase, phase_clean, albedo_clean,
            p0=initial_guess, bounds=bounds, maxfev=100000
        )
        fitted = akimov_phase(phase_clean, *params)
        residuals = albedo_clean - fitted
        rss = np.sum(residuals**2)
        tss = np.sum((albedo_clean - np.mean(albedo_clean))**2)
        r2 = 1 - rss / tss if tss > 0 else np.nan
        errors = np.sqrt(np.diag(cov))
        return params, errors, rss, r2
    except:
        print(f"Fit error: {e}")
        return None

@profile
def main():
    script_dir = Path(__file__).resolve().parent
    data_file = script_dir / "binned_albedo_per_image.npz"

    with np.load(data_file) as data:
        aeq_mean = data["aeq_mean"]
        phase_mean = data["phase_mean"]
        lat_centers = data["lat_centers"]
        lon_centers = data["lon_centers"]

    num_lat, num_lon, _ = aeq_mean.shape
    shape = (num_lat, num_lon)

    # Initialize local result arrays
    local_out = {k: np.full(shape, np.nan) for k in [
        'A', 'nu1', 'm', 'nu2', 'A_err', 'nu1_err', 'm_err', 'nu2_err', 'rss', 'r2'
    ]}

    initial_guess = [0.07, 0.02, 0.3, 0.2]
    bounds = ([0.0, 0.0, 0.0, 0.0], [0.2, 0.1, 2, 1])

    # Divide the grid: each rank gets a subset of lat indices
    lat_indices = list(range(num_lat))
    lat_chunks = np.array_split(lat_indices, size)
    my_chunk = lat_chunks[rank]

    # === Fitting ===
    for i in my_chunk:
        for j in range(num_lon):
            result = fit_akimov_model(
                phase_mean[i, j, :], aeq_mean[i, j, :],
                initial_guess, bounds
            )
            if result:
                params, errors, rss, r2 = result
                local_out['A'][i, j], local_out['nu1'][i, j], local_out['m'][i, j], local_out['nu2'][i, j] = params
                local_out['A_err'][i, j], local_out['nu1_err'][i, j], local_out['m_err'][i, j], local_out['nu2_err'][i, j] = errors
                local_out['rss'][i, j] = rss
                local_out['r2'][i, j] = r2

            #plot_fit(phase_clean, albedo_clean, fitted, params, errors, f'bin_fits/{i}_{j}.png')

    # === Gather and Reduce Results to Rank 0 ===
    def gather_all(name):
        arr = np.empty_like(local_out[name])
        comm.Reduce(local_out[name], arr, op=MPI.SUM, root=0)
        return arr

    if rank == 0:
        final_out = {k: gather_all(k) for k in local_out}
        np.savez_compressed(
            script_dir / "akimov_fit_gridded_mpi.npz",
            **{k: final_out[k] for k in final_out}
        )
    else:
        for k in local_out:
            comm.Reduce(local_out[k], None, op=MPI.SUM, root=0)

if __name__ == '__main__':

    # === MPI Setup ===
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if rank == 0: start_time = time.time()

    main()

    if rank == 0: print(f'Completed in {time.time()-start_time}')
