# URDF-X: Enhancing the Physical Simulation of Articulated Objects via the Collision Mesh Optimization and Joint Parameter Correction

**URDF-X** is a plug-and-play enhancement module that optimizes collision meshes through an innovative EdgeCNN architecture and introduces a simulation-guided joint parameter correction system. 

---

## Main Workflow

1. **Create a Conda Environment**  
   Set up a dedicated conda environment to manage all dependencies:
   ```bash
   conda create -n urdfx-env python=3.8
   conda activate urdfx-env
    ```
2. **Install Python Dependencies**  
   Install the required packages using the provided requirements.txt:
   ```bash
   pip install -r requirements.txt
    ```
   
3. **Import Your 3D Asset or URDF File**  
   Place the 3D asset (in supported formats) or URDF file that you wish to optimize into the designated input directory.
   
4. **Run the Main Script**  
   Execute the main processing script to start the optimization process:
   ```bash
   python main.py --input path/to/your/input.file --output path/to/your/output.file
    ```
### Getting Help
If you encounter any issues or have suggestions for improvement, please feel free to contact us or open an issue in the repository.
