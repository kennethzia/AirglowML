Using LightGBM's Python API for Machine Learning (ML) Applications

1) Produce a labeled data set of ~equal amounts good and bad data ("LabeledImages") of a season.

2) Produce a LightGBM model from labeled data with "MachineLearning.py".

3) Apply the model to new data from the same instrument/station with "ASICleaning.py".

4) Use "MLshellrunner.pro" with section commented out as mentioned in code to sort through frames catagorized as '0' or '1' to find clean windows of >2 hours for spectral analysis.

5) Days that are found to have viable data windows need to be processed with the *French Flag Program* to be calibrated, flat-fielded, and unwarped into a "Processed" folder with the file name "OH_ff****.tif" for each frame #****.

6) Use IDL code (compiled in order) "m_fft_asi.pro", "read_images.pro", and "MLshellrunner.pro" to perform 3-D FFT wave analysis.
	Resulting power spectrums are saved in desktop file with year and station name. Only edits need to be made in "MLshellrunner.pro". 
	Check variables at top of code before running - 'savefilelocation', 'readfilelocation', 'Year', and 'monthsArray'.
7) The Python code "FigureMaker.py" is used to make the resulting figures with mean phase velocity Power Spectrum Densities (PSD) for each day and a monthly average, as well as a daily total power.

8) Write up results and publish!