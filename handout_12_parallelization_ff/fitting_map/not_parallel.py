import numpy as np
from pathlib import Path
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from line_profiler import profile
import time 

# === Models ===
def linear_exp(phase, A, d, b, k):
    alpha = np.radians(phase)
    return A * np.exp(-phase / d) + b - k * phase

def akimov_phase(phase, A, nu1, m, nu2):
    return A * (np.exp(-nu1 * phase) + m * np.exp(-nu2 * phase)) / (1 + m)


# === Utility functions ===
def initialize_output_arrays(shape):
    keys = ['A', 'nu1', 'm', 'nu2', 'A_error', 'nu1_error', 'm_error', 'nu2_error', 'rss', 'r2']
    return {k: np.full(shape, np.nan) for k in keys}

@profile
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
    except Exception as e:
        print(f"Fit error: {e}")
        return None

    fitted = akimov_phase(phase_clean, *params)
    residuals = albedo_clean - fitted
    rss = np.sum(residuals**2)
    tss = np.sum((albedo_clean - np.mean(albedo_clean))**2)
    r2 = 1 - rss / tss if tss > 0 else np.nan
    errors = np.sqrt(np.diag(cov))

    return params, errors, rss, r2, phase_clean, albedo_clean, fitted


# === Main Script ===
@profile
def main():
    script_dir = Path(__file__).resolve().parent
    data_file = script_dir / "binned_albedo_per_image.npz"

    with np.load(data_file) as data:
        aeq_mean = data["aeq_mean"]
        phase_mean = data["phase_mean"]
        count = data["count"]
        lat_centers = data["lat_centers"]
        lon_centers = data["lon_centers"]

    num_lat, num_lon, num_images = aeq_mean.shape
    output = initialize_output_arrays((num_lat, num_lon))

    initial_guess = [0.07, 0.02, 0.3, 0.2]
    bounds = ([0.0, 0.0, 0.0, 0.0], [0.2, 0.1, 2, 1])

    for i in range(num_lat):
        for j in range(num_lon):
            result = fit_akimov_model(
                phase_mean[i, j, :], aeq_mean[i, j, :],
                initial_guess, bounds
            )

            if result is None:
                continue

            params, errors, rss, r2, phase_clean, albedo_clean, fitted = result
            output['A'][i, j], output['nu1'][i, j], output['m'][i, j], output['nu2'][i, j] = params
            output['A_error'][i, j], output['nu1_error'][i, j], output['m_error'][i, j], output['nu2_error'][i, j] = errors
            output['rss'][i, j] = rss
            output['r2'][i, j] = r2

    # Save output
    np.savez_compressed(script_dir / "akimov_fit_gridded.npz", **output)

if __name__ == '__main__':
    
    start_time = time.time()
    
    main()
    
    print(f'Completed in {time.time()-start_time}')



