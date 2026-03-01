Urban Growth & Change Detection: Chennai Metropolitan Area (2014–2035)
Project Overview
This project analyzes the rapid urbanization of Chennai using Remote Sensing and Machine Learning. By processing multi-temporal satellite data, I mapped Land Use and Land Cover (LULC) changes from 2014 to 2024 and predicted future urban footprints for 2035.

Key Technical Highlights
Platform: Google Earth Engine (GEE)

Data Source: Landsat 8 & Landsat 9 Satellite Imagery

Classifier: Random Forest (Achieved 99.59% Overall Accuracy)

Prediction Model: CA-Markov (Cellular Automata-Markov Chain)

Categories: Water Bodies, Urban (Built-up), and Vegetation.

Analysis & Results
2014–2024 Growth: Urban area expanded by 57.92 sq km in a decade.

2035 Prediction: Projected to grow by another 63.69 sq km.

Final Footprint: Chennai's urban area is estimated to reach 484.78 sq km by 2035.

Project Structure
Plaintext
├── Data/               # Pre-processed Satellite Tiff files

├── Scripts/            # GEE JavaScript/Python API codes

├── Results/            # Classified Maps & Accuracy Reports

└── README.md           # Project Documentation

Methodology
Preprocessing: Cloud masking and median composite generation in GEE.

Classification: Training the Random Forest model using high-quality ground truth points.

Change Detection: Post-classification comparison to derive the transition matrix.

Simulation: Using CA-Markov for future spatial growth modeling.

How to Use
Open Google Earth Engine Code Editor.

Copy the script from Scripts/Urban_Analysis.js.

Select the Area of Interest (AOI) as Chennai.

Run the script to visualize LULC maps and accuracy metrics.

Contact
If you have any questions or want to collaborate, feel free to reach out via GitHub or LinkedIn!
