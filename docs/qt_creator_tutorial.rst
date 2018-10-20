QT Creator configuration for stm32
==================================

This short tutorial describes how to configure *Qt Creator* for project that is produced with
the `STM32CubeMX <http://www.st.com/en/development-tools/stm32cubemx.html>`_.

Configuration steps
-------------------

#. Select **Help** > **About Plugins** > **Device Support** > **Bare Metal**

   .. image:: images/qt_creator/pic_1_plugin.png

#. Restart qt creator

#. Select **Tools** > **Options** > **Devices** > **Bare Metal** and create OpenOCD configuration for your board.
   Note that you should set **configuration file** for your board.

   .. image:: images/qt_creator/pic_2_bare_metal_openocd.png

#. Select **Devices** and add device configuration using configuration from previous step.

   .. image:: images/qt_creator/pic_3_bare_metal_device.png

#. Select **Tools** > **Options** > **Build & Run** > **Compilers** and add *arm-gcc* C/C++ compilers.

   .. image:: images/qt_creator/pic_4_run_and_build_compilers.png

#. Go to **Debugger** tab and add *arm-gcc* debugger.

   .. image:: images/qt_creator/pic_5_run_and_build_debugger.png

#. Go to **Kit** tab and create new *Kit* for the board.

   .. image:: images/qt_creator/pic_6_run_and_build_kit.png

   the following options should be adjusted:

   - Device type
   - Device
   - Compiler
   - Debugger
   - Qt version (should be set to None)
   - CMake Configuration

   In the **CMake Configuration** you should set ``CMAKE_FORCE_C_COMPILER`` and ``CMAKE_FORCE_CXX_COMPILER`` to prevent
   compiler validation, as ``arm-none-eabi-gcc`` cannot compile ordinary desktop programs::

     CMAKE_CXX_COMPILER_FORCED:BOOL=ON
     CMAKE_C_COMPILER_FORCED:BOOL=ON


   .. image:: images/qt_creator/pic_7_run_and_build_kit_cmake.png

   .. note:: If you use some string parameter in the **CMake Configuration**, you shouldn't
             escape it with quotes. For example you should write ``PROJECT_OPTIMIZATION_FLAGS:STRING=-g -O0``
             instead of ``PROJECT_OPTIMIZATION_FLAGS:STRING="-g -O0"``

#. Go to **Genera** tab and change "Default build directory" to ``build/%{CurrentBuild:Name}`` (optional)

   .. image:: images/qt_creator/pic_8_run_and_build_general.png

#. Open STM32CubeMX and create new "make" project.

   .. image:: images/qt_creator/pic_9_cubemx.png

   .. note:: ensure that pins for debug interface are enabled. Otherwise after first program
             uploading you won't be able to reprogram an microcontroller.

#. Run from project folder the command to create ``CMakeLists.txt`` file::

      vznncv-cubemx generate-cmake-project

#. Adjust **openocd_stm.cfg** for your configuration (optional).

#. Open Qt Creator, select **File** > **Open File or Project ...* and open created ``CMakeLists.txt`` file.
   When Qt Creator ask to configure project, select created *kit* configuration and configure project.

   .. image:: images/qt_creator/pic_10_qt_import_project.png

#. Run **Build** > **Run CMake** and **Build** > **Build project "..."**. If there are no errors, you will find
    binary, hex and elf file in the "build" directory

#. If you use Qt Creator 4.6, please select **Projects** > **Build & Run** > **<your_kit>** > **Run** and
   manually add **Custom Executable (on GDB server or hardware debugger)**.
   For details see issue `QTCREATORBUG-20317 <https://bugreports.qt.io/browse/QTCREATORBUG-20317?attachmentOrder=desc>`_.

   .. image:: images/qt_creator/pic_11_qt_run_config.png

#. Now you can debug your application.

   .. image:: images/qt_creator/pic_12_qt_debug.png

Steps 1-8 should be done once for each board/chip. The steps 8-12 should be repeated for each project.

Upload application without debugging
------------------------------------

By default qt creator doesn't have such option, but you can add external tool for elf file uploading.

Links
-----

* `Qt Creator. Connecting Bare Metal Devices <http://doc.qt.io/qtcreator/creator-developing-baremetal.html>`_
* `Qt Creator with mbed-os <https://os.mbed.com/users/hudakz/notebook/building-offline-with-qt-creator/>`_
