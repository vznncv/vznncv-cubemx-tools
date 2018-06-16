from hamcrest import assert_that, has_properties, has_items, contains_inanyorder
from os.path import join, dirname

from testing_utils import BaseTestCase as TestCase
from vznncv.cubemx.tools._make_parser import parse_variables
from vznncv.cubemx.tools._project_description import build_project_description


class MakeParserTestCase(TestCase):
    def test_make_parsing_stm32f3(self):
        makefile = join(self.FIXTURE_DIR, 'stm32f3_project', 'Makefile')
        makefile_vars = parse_variables(makefile)

        project_description = build_project_description(
            makefile_vars,
            project_dir=dirname(makefile),
            optimization_flags=['-Og']
        )

        assert_that(project_description, has_properties(
            build_dir='build',
            target='DemoProject',
            stm_series='stm32f3',

            source_files=has_items('Drivers/STM32F3xx_HAL_Driver/Src/stm32f3xx_hal.c', 'Src/stm32f3xx_it.c'),
            include_dirs=has_items('Drivers/STM32F3xx_HAL_Driver/Inc', 'Inc'),
            definitions=contains_inanyorder('STM32F303xC', 'USE_FULL_LL_DRIVER', 'USE_HAL_DRIVER'),

            mcu_flags=contains_inanyorder('-mcpu=cortex-m4', '-mthumb', '-mfpu=fpv4-sp-d16', '-mfloat-abi=hard'),

            optimization_flags=contains_inanyorder('-Og'),

            ld_script='STM32F303VCTx_FLASH.ld'
        ))

    def test_make_parsing_stm32f1(self):
        makefile = join(self.FIXTURE_DIR, 'stm32f1_project', 'Makefile')
        makefile_vars = parse_variables(makefile)

        project_description = build_project_description(
            makefile_vars,
            project_dir=dirname(makefile),
            optimization_flags=['-Og']
        )

        assert_that(project_description, has_properties(
            build_dir='build',
            target='cubmex_stm32f1_demo',
            stm_series='stm32f1',

            source_files=has_items('Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal.c', 'Src/stm32f1xx_it.c'),
            include_dirs=has_items('Drivers/STM32F1xx_HAL_Driver/Inc', 'Inc'),
            definitions=contains_inanyorder('STM32F103xB', 'USE_HAL_DRIVER'),

            mcu_flags=contains_inanyorder('-mcpu=cortex-m3', '-mthumb'),

            optimization_flags=contains_inanyorder('-Og'),

            ld_script='STM32F103C8Tx_FLASH.ld'
        ))
