# Check logging configuration
import os
import logging

print('Environment variables:')
print(f"  RASALOG = {os.environ.get('RASALOG', 'NOT SET')}")
print(f"  LOG_LEVEL_LLM_COMMAND_GENERATOR = {os.environ.get('LOG_LEVEL_LLM_COMMAND_GENERATOR', 'NOT SET')}")

# Check root logger level
print()
print('Root logger level:', logging.getLogger().level)

# Check rasa logger level
rasa_logger = logging.getLogger('rasa')
print('Rasa logger level:', rasa_logger.level)

# Check specific logger
llm_logger = logging.getLogger('rasa.dialogue_understanding.generator.single_step.single_step_based_llm_command_generator')
print('LLM CG logger level:', llm_logger.level)

# Test if DEBUG is enabled
print()
print('Is DEBUG enabled for LLM CG?', llm_logger.isEnabledFor(logging.DEBUG))