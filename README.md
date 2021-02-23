# VU.CITY

**How to use the VU.CITY Blender plugin**
1. Save the .py file anywhere on your machine. 
2. Open Blender and go to Edit->Preferences->Add-ons->Install.
3. Find and select the VUCITY Plugin.py file you downloaded.
4. Enable the add-on by selecting the box.
5. Now in Blender's 3D scene if you press N, you'll find the VU.CITY add-on appear on the right hand side of the 3D view.

**Button Descriptions**
1. _Start Here_
   - **Select & Merge Meshes**: Selects the objects and merges them into one. This option must be enabled in order for the following operations to work.
   - **Rotate by 90°**: Flips X-rotation by 90°
   
2. _Optimise / Reduce Detail _
   - **High**: Collapse vertices by distance of 10 cm
   - **Medium**: Collapse vertices by distance of 5 cm (recommended)
   - **Low**: Collapse vertices by distance of 1 cm

3. _Zero & Geolocate Model_
   - **Origin to Geometry**: Sets the origin to a point on the base of the model
   - **Zero Model**: Moves the model to world zero (0, 0, 0)
   - **Geolocate**: After completing the above to operations, you can now enter your Eastings, Northings and AOD / Height coordinates into the X, Y, Z fields respectively to geolcate your model.

4. _Appearance_
   - **Fix Shading Smudges**: Fixes smooth shading issues / dark smudges
   - **Remove Materials**: Removes all materials associated with the model

5. _Rescale Model_
   - **Scale x0.1**: Decreases the scale of your model by factor 10
   - **Scale x.10**: Increases the scale of your model by factor 10
  
6. _Adjust Faces_
   - **Reveal Flipped Faces**: Reveals flipped faces
   - **Correct Flipped Faces**: Recalculates normals to correct flipped faces (Experimental)
   - **Triangulate N-gons and Quads**: Translates n-gons & quads to tris
     

**System requirements**
1. Blender 2.9 or above


