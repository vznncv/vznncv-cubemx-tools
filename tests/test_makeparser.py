from hamcrest import assert_that, has_entries, all_of, contains_string
from os.path import join

from testing_utils import BaseTestCase as TestCase
from vznncv.cubemx.tools._make_parser import parse_variables


class MakeParserTestCase(TestCase):
    def test_variable_parsing(self):
        makefile = join(self.FIXTURE_DIR, 'stm_project', 'Makefile')
        makefile_vars = parse_variables(makefile)

        assert_that(makefile_vars, has_entries({
            'TARGET': 'DemoProject',
            'C_SOURCES': all_of(contains_string('Src/main.c'),
                                contains_string('Middlewares/Third_Party/FreeRTOS/Source/queue.c')),
            'ASM_SOURCES': 'startup_stm32f303xc.s',

            'MCU': '-mcpu=cortex-m4 -mthumb -mfpu=fpv4-sp-d16 -mfloat-abi=hard',
            'AS_DEFS': '',
            'C_DEFS': '-DUSE_FULL_LL_DRIVER -DUSE_HAL_DRIVER -DSTM32F303xC',
            'AS_INCLUDES': '',
            'C_INCLUDES': '-IInc '
                          '-IDrivers/STM32F3xx_HAL_Driver/Inc '
                          '-IDrivers/STM32F3xx_HAL_Driver/Inc/Legacy '
                          '-IDrivers/CMSIS/Device/ST/STM32F3xx/Include '
                          '-IDrivers/CMSIS/Include '
                          '-IMiddlewares/Third_Party/FreeRTOS/Source/portable/GCC/ARM_CM4F '
                          '-IMiddlewares/Third_Party/FatFs/src '
                          '-IMiddlewares/Third_Party/FreeRTOS/Source/include '
                          '-IMiddlewares/Third_Party/FreeRTOS/Source/CMSIS_RTOS',
            'LDSCRIPT': 'STM32F303VCTx_FLASH.ld',
        }))
