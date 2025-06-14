import matplotlib.pyplot as plt
import numpy as np
import os

def _plot_explanation_analysis(explanations, output_dir):

    if isinstance(output_dir, dict):
        output_dir = output_dir["visualization_dir"]
    
    os.makedirs(output_dir, exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    risk_levels = [data['risk_classification'] for data in explanations.values()]
    probabilities = [data['probability'] for data in explanations.values()]

    # 1. Risk Classification Distribution
    risk_counts = {}
    for risk in risk_levels:
        risk_counts[risk] = risk_counts.get(risk, 0) + 1

    colors_map = {
        'Resiko Tinggi': 'red',
        'Resiko Sedang': 'orange',
        'Resiko Rendah (Top Candidate)': 'green'
    }
    colors = [colors_map.get(risk, 'gray') for risk in risk_counts.keys()]

    ax1.bar(risk_counts.keys(), risk_counts.values(), color=colors, alpha=0.7)
    ax1.set_title('Risk Level Distribution', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Number of Users')
    ax1.tick_params(axis='x', rotation=45)

    # 2. Probability Histogram
    ax2.hist(probabilities, bins=10, color='skyblue', alpha=0.7, edgecolor='black')
    ax2.set_title('Insider Probability Distribution\n(Analyzed Users)', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Insider Probability')
    ax2.set_ylabel('Number of Users')
    
    mean_prob = np.mean(probabilities)
    ax2.axvline(mean_prob, color='red', linestyle='--', label=f'Mean: {mean_prob:.3f}')
    ax2.legend()

    plt.tight_layout()
    save_path = os.path.join(output_dir, 'explanation_analysis.png')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"[✔] Explanation analysis plot")
