
# 🧭 Hexify

**Hexify** is a simple GUI-based Python application that converts a CSV file containing H3 hexagon IDs into a GIS-compatible GeoPackage file. It allows users to specify the hex ID column and output layer name, and handles the geometry creation and file export automatically.

---


## 🖥️ Features

- 📂 Select input CSV file via GUI
- 🔢 Specify the column containing H3 hex IDs
- 🗂️ Define the output layer name
- 🗺️ Automatically generates geometries from hex IDs
- 💾 Saves the output as a `.gpkg` (GeoPackage) file

---


## 📦 Requirements

- Python 3.8+
- `tkinter`
- `pandas`
- `geopandas`
- `h3`

---

## Installation

### 1. Download Hexify
Pull Guss repository or download and extract the zip folder to your desired project directory

### 2. Create a Virtual Environment
Navigate to your project directory in your terminal. Then, run the following command to create a new virtual environment:

```
python -m venv venv
```
- venv is the name of the virtual environment folder. You can replace it with any name you prefer, but venv is commonly used.
- This command will create a folder called venv in your project directory containing the Python environment.

### 3. Activate the Virtual Environment
After creating the virtual environment, you need to activate it:

#### On macOS/Linux:
```
source venv/bin/activate
```
#### On Windows:
```
venv\Scripts\activate
```
Once activated, you’ll notice the environment name (e.g., (venv)) appears in the terminal prompt, indicating that the virtual environment is active.

### 4. Install Dependencies from requirements.txt
Now, with the virtual environment activated, you can install the required dependencies listed in your requirements.txt file.

Ensure that you have a requirements.txt file in your project folder, and that it contains the necessary dependencies

To install the dependencies, run:

```
pip install -r requirements.txt
```


## 🏃‍♂️ Run the Application

Navigate to the project directory and run:

```bash
python app.py
```

This will launch the **Hexify GUI**.

---

## 🖱️ Using the GUI

1. **Browse**: Select your input CSV file.
2. **Hex ID Column Name**: Enter the name of the column in your CSV that contains H3 hex IDs (e.g., `hex_id`).
3. **Output Layer Name**: Enter the desired name for the output GIS layer.
4. **Process and Save**: Click the button to generate and save the GeoPackage file.

A progress dialog will appear showing the current status of the operation.

---

## 📤 Output

- The output will be saved as a `.gpkg` (GeoPackage) file.
- The output file can be opened in GIS software like **QGIS** or **ArcGIS**.



## 🛠️ Troubleshooting

- Ensure your CSV contains valid H3 hex IDs.
- If you get an error about missing columns, double-check the column name you entered.
- If the app crashes or freezes, make sure to End-Task from the task manager and restart the application.
---

## 📬 Questions or Feedback?

Feel free to open an issue or contribute to the project!
