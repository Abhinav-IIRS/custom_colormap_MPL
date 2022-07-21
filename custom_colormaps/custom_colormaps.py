"""
NAME
    Custom Colormaps for Matplotlib
PURPOSE
    This program shows how to implement make_cmap which is a function that
    generates a colorbar
PROGRAMMER(S)
    Chris Slocum
REVISION HISTORY
    20130411 -- Initial version created
    20140313 -- Small changes made and code posted online
    20140320 -- Added the ability to set the position of each color
    20150724 -- Attempted to make this more Pythonic
    20180307 -- Changed license to BSD 3-clause
"""
'''
Original code by Chris Slocum

Modified by Abhinav Sharma for added NCAR-NCL colormap support.

Reference : https://github.com/CSlocumWX/custom_colormap
'''

import numpy as np

def create_colormap(colors, position=None, bit=False, reverse=False, name='custom_colormap'):
    """
    returns a linear custom colormap

    Parameters
    ----------
    colors : array-like
        contain RGB values. The RGB values may either be in 8-bit [0 to 255]
        or arithmetic [0 to 1] (default).
        Arrange your tuples so that the first color is the lowest value for the
        colorbar and the last is the highest.
    position : array like
        contains values from 0 to 1 to dictate the location of each color.
    bit : Boolean
        8-bit [0 to 255] (in which bit must be set to
        True when called) or arithmetic [0 to 1] (default)
    reverse : Boolean
        If you want to flip the scheme
    name : string
        name of the scheme if you plan to save it

    Returns
    -------
    cmap : matplotlib.colors.LinearSegmentedColormap
        cmap with equally spaced colors
    """
    from matplotlib.colors import LinearSegmentedColormap
    if not isinstance(colors, np.ndarray):
        colors = np.array(colors, dtype='f')
    if reverse:
        colors = colors[::-1]
    if position is not None and not isinstance(position, np.ndarray):
        position = np.array(position)
    elif position is None:
        position = np.linspace(0, 1, colors.shape[0])
    else:
        if position.size != colors.shape[0]:
            raise ValueError("position length must be the same as colors")
        elif not np.isclose(position[0], 0) and not np.isclose(position[-1], 1):
            raise ValueError("position must start with 0 and end with 1")
    if bit:
        colors[:] = [tuple(map(lambda x: x / 255., color)) for color in colors]
    cdict = {'red':[], 'green':[], 'blue':[]}
    for pos, color in zip(position, colors):
        cdict['red'].append((pos, color[0], color[0]))
        cdict['green'].append((pos, color[1], color[1]))
        cdict['blue'].append((pos, color[2], color[2]))
    return LinearSegmentedColormap(name, cdict, 256)


def colormap_tuple(RGB_file,return_tuple = True, return_cmap = False, headers=0,footers=0,delimiter=None):
    '''
    Retrun a list of tuple with RGB values
    Parameters
    ----------
    RGB_file : text file
        RGB textfile with coloumns value as R G B.
    return_tuple : logical, optional
        Return a tuple with RGB values. The default is True.
    return_cmap : logical, optional
        Returns the cmap directly from RGB file using create_colormap under the hood. The default is False.
    headers : int, optional
        Number of headers to skip. The default is 0.
    footers : TYPE, optional
        Number of footers to skip. The default is 0.
    delimiter : TYPE, optional
        Delimiter in text file. The default is None.

    Returns
    -------
    list
        List of tuple with each RGB values in 256 segments.
    '''

    import numpy as np
    txt_array = np.genfromtxt(RGB_file,skip_header = headers, skip_footer = footers, delimiter = delimiter)
    if return_cmap == True:
        cmap = create_colormap([tuple((txt_array[i,0],txt_array[i,1],txt_array[i,2])) for i in range(0,txt_array.shape[0])], bit = True)
        return cmap
    return [tuple((txt_array[i,0],txt_array[i,1],txt_array[i,2])) for i in range(0,txt_array.shape[0])]



def NCAR_RGB_pull(cmap_name,save_loc = None):
    '''
    Module to download NCL NCAR colormaps RGB file.
    Files downloaded can be made into LinearSegmented colormaps using create_colormap function.
    
    Parameters
    ----------
    cmap_name : str
        Name of NCL-NCAR colormap to be downloaded.
    save_loc : str, optional
        Directory to save RGB file. If not provided, file is saved in the present working directory. The default is None.

    Returns
    -------
        Print message for download complete information.
    '''
    
    import requests
    import shutil
    import os
    cmap_name = cmap_name
    address = 'https://www.ncl.ucar.edu/Document/Graphics/ColorTables/Files/'
    url = address+cmap_name
    local_filename = url.split('/')[-1]
    if save_loc == None:
        with requests.get(url, stream=True) as r:
            with open(local_filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        print("Download complete for : "+local_filename)
        print("File saved in : \n"+os.getcwd())
    else:
        with requests.get(url, stream=True) as r:
            with open(save_loc+local_filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        print("Download complete for : "+local_filename)
        print("File saved in : \n"+save_loc)


if __name__ == "__main__":
    # An example of how to use make_cmap
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(311)
    # Create a list of RGB tuples
    colors = [(255, 0, 0), (255, 255, 0), (255, 255, 255), (0, 157, 0), (0, 0, 255)] # This example uses the 8-bit RGB
    # Call the function make_cmap which returns your colormap
    my_cmap = create_colormap(colors, bit=True)
    # Use your colormap
    plt.pcolor(np.random.rand(25, 50), cmap=my_cmap)
    plt.colorbar()
    ax = fig.add_subplot(312)
    colors = [(1, 1, 1), (0.5, 0, 0)] # This example uses the arithmetic RGB
    # If you are only going to use your colormap once you can
    # take out a step.
    plt.pcolor(np.random.rand(25, 50), cmap=create_colormap(colors))
    plt.colorbar()

    ax = fig.add_subplot(313)
    colors = [(0.4, 0.2, 0.0), (1, 1, 1), (0, 0.3, 0.4)]
    # Create an array or list of positions from 0 to 1.
    position = [0, 0.3, 1]
    plt.pcolor(np.random.rand(25, 50), cmap=create_colormap(colors, position=position))
    plt.colorbar()
    plt.savefig("example_custom_colormap.png")
    plt.show()
