#PyGEOMET setup.py file
import sys
import os
from Cython.Build import cythonize

#Switch to True to compile with CRTM
#CRTM can be downloaded at: http://ftp.emc.ncep.noaa.gov/jcsda/CRTM/
USE_CRTM = False
#Set the crtm_path once CRTM has been compiled
crtm_path = "/home/usr/CRTM"
crtm_include = crtm_path+"/include"
crtm_lib = "-L"+crtm_path+"/lib -lCRTM"
#Must specify the fortran compiler to be the same one used to 
#  compile CRTM. This is done during the install. 
# example : python setup.py config --fcompiler=pg install
# where pg is a pgi fortran compiler. Default is gfortran

### ACTUAL SETUP VALUES ###
name = "PyGEOMET"
version = '1.0.0'
author = "Andrew White, Brian Freitag and Udaysankar Nair"
author_email = "andrew.white@nsstc.uah.edu, brian.freitag@nsstc.uah.edu, nair@nsstc.uah.edu"
description = "Python GUI for Earth Observations and Modeling Evaluation Toolkit"
long_description = ""
license = "GPL"
keywords = "numerical modeling, atmospheric science"
url = "https://github.com/pygeomet/PyGEOMET"
packages = ['PyGEOMET','PyGEOMET.datasets', 'PyGEOMET.icons', 'PyGEOMET.utils']
package_data = {"PyGEOMET.icons": ["down.png"],"PyGEOMET.utils":["radar_sites.csv"]}
classifiers = ["Development Status :: 3 - Alpha",
               "Programming Language :: Python :: 3.6,3.5,2.7",]

#Check to see if the user enable CRTM
#**Note: CRTM must be compiled by the user separately before using 
#        within PyGEOMET. Also, we haven't found an easy way to do this on Windows.
if USE_CRTM:
    #Check to make sure the user has provided correct paths to CRTM
    if (os.path.isdir(crtm_path)):
        #numpy.distutils is used over setuptools due to f2py support
        from numpy.distutils.core import setup
        from numpy.distutils.extension import Extension
        extensions = [Extension("PyGEOMET.utils.wrf_cython",["PyGEOMET/utils/wrf_cython.pyx"],
                                extra_compile_args = ["-ffast-math"]), 
                      Extension("PyGEOMET.utils.crtm_python",["PyGEOMET/utils/crtm_python.f90"],
                                include_dirs=[crtm_include],
                                extra_link_args = [crtm_lib])]
        setup(
              name = name,
              version = version,
              author = author,
              author_email = author_email,
              description = description,
              long_description = long_description,
              license = license,
              keywords = keywords,
              url = url,
              packages = packages,
              package_data = package_data,
              ext_modules = cythonize(extensions),                       
              classifiers = classifiers
             )
    else:
        print("****Specified CRTM path does not exist****")
        print("****Please set the path within the setup.py file and try again****")
        sys.exit()
else: 
    #Use setuptools if not compiling with f2py 
    #Seems to work better with Windows
    from setuptools import setup
    from setuptools.extension import Extension    
    extensions = [Extension("PyGEOMET.utils.wrf_cython",["PyGEOMET/utils/wrf_cython.pyx"],
                            extra_compile_args = ["-ffast-math"])]
    setup(
          name = name,
          version = version,
          author = author,
          author_email = author_email,
          description = description,
          long_description = long_description,
          license = license,
          keywords = keywords,
          url = url,
          packages = packages,
          package_data = package_data,
          include_package_data=True,
          ext_modules = cythonize(extensions),                       
          classifiers = classifiers
         )
