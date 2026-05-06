Your input ->  Jeffrey epstein esta vivo?                                                                                                                                   
2026-05-05 14:15:33 DEBUG    rasa.core.lock_store  - [debug    ] Issuing ticket for conversation 'ad2a1a1e1edc41b6882b7d80757e1135'. event_key=lock_store.issue_ticket
2026-05-05 14:15:33 DEBUG    rasa.core.lock_store  - [debug    ] Acquiring lock for conversation 'ad2a1a1e1edc41b6882b7d80757e1135'. event_key=lock_store._acquiring_lock_for_conversation
2026-05-05 14:15:33 DEBUG    rasa.core.lock_store  - [debug    ] Acquired lock for conversation 'ad2a1a1e1edc41b6882b7d80757e1135'. event_key=lock_store._acquired_lock_for_conversation
2026-05-05 14:15:33 DEBUG    rasa.engine.runner.dask  - [debug    ] Running graph with inputs, targets and execution context. event_key=rasa.engine.runner.dask.run execution_context=ExecutionContext(model_id='a076f846c70a4d269ab37f3809ece1d8', should_add_diagnostic_data=False, is_finetuning=False, node_name=None) inputs={} targets=['flows_provider']
2026-05-05 14:15:33 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-05-05 14:15:33 DEBUG    rasa.engine.runner.dask  - [debug    ] Running graph with inputs, targets and execution context. event_key=rasa.engine.runner.dask.run execution_context=ExecutionContext(model_id='a076f846c70a4d269ab37f3809ece1d8', should_add_diagnostic_data=False, is_finetuning=False, node_name=None) inputs={'__message__': [<rasa.core.channels.channel.UserMessage object at 0x00000226FBBBACD0>], '__tracker__': DialogueStateTracker(sender_id: ad2a1a1e1edc41b6882b7d80757e1135)} targets=['run_RegexMessageHandler']
2026-05-05 14:15:33 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=NLUMessageConverter fn=convert_user_message node_name=nlu_message_converter
2026-05-05 14:15:33 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=WhitespaceTokenizer fn=process node_name=run_WhitespaceTokenizer0
2026-05-05 14:15:33 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=RegexFeaturizer fn=process node_name=run_RegexFeaturizer1
2026-05-05 14:15:33 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=KeywordIntentClassifier fn=process node_name=run_KeywordIntentClassifier2
2026-05-05 14:15:33 DEBUG    rasa.nlu.classifiers.keyword_intent_classifier  - KeywordClassifier did not find any keywords in the message.
2026-05-05 14:15:33 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-05-05 14:15:33 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DomainProvider fn=provide_inference node_name=domain_provider
2026-05-05 14:15:33 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=NLUCommandAdapter fn=process node_name=run_NLUCommandAdapter3
2026-05-05 14:15:33 DEBUG    rasa.dialogue_understanding.utils  - [debug    ] Tracker doesn't have the 'route_session_to_calm' slot.Routing to CALM. event_key=utils.handle_via_nlu_in_coexistence.tracker_missing_route_session_to_calm_slot route_session_to_calm=[]
2026-05-05 14:15:33 DEBUG    rasa.dialogue_understanding.generator.nlu_command_adapter  - [debug    ] nlu_command_adapter.available_slot_names available_slot_names={'continue_interrupted_flow_confirmation', 'continue_conversation', 'interrupted_flow_to_continue'}
2026-05-05 14:15:33 DEBUG    rasa.dialogue_understanding.generator.nlu_command_adapter  - [debug    ] nlu_command_adapter.predict_commands commands=[]
2026-05-05 14:15:33 DEBUG    rasa.dialogue_understanding.generator.nlu_command_adapter  - [debug    ] nlu_command_adapter.predict_commands.finished commands=[]
2026-05-05 14:15:33 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=CompactLLMCommandGenerator fn=process node_name=run_CompactLLMCommandGenerator4
2026-05-05 14:15:33 DEBUG    rasa.dialogue_understanding.utils  - [debug    ] Tracker doesn't have the 'route_session_to_calm' slot.Routing to CALM. event_key=utils.handle_via_nlu_in_coexistence.tracker_missing_route_session_to_calm_slot route_session_to_calm=[]
2026-05-05 14:15:33 DEBUG    rasa.shared.providers.embedding._base_litellm_embedding_client  - [debug    ] base_litellm_client.formatted_response formatted_response={'data': 'Embedding response data not shown here for brevity.', 'model': 'ollama/nomic-embed-text:latest', 'usage': {'prompt_tokens': 8, 'completion_tokens': 0, 'total_tokens': 8}, 'additional_info': None}
2026-05-05 14:15:33 DEBUG    rasa.dialogue_understanding.generator.flow_retrieval  - [debug    ] Fetched the top 20similar flows from the vector store event_key=flow_retrieval.query_vector_store.fetched query='Jeffrey epstein esta vivo?' results=[{'flow_id': 'saludo', 'score': np.float32(0.6676324), 'content': 'saludo: Saludar al usuario e iniciar la conversación de auditoría farmacéutica.'}, {'flow_id': 'consulta_auditoria', 'score': np.float32(0.58968955), 'content': 'consulta auditoria: Atender una consulta normativa o de auditoría farmacéutica delegando la respuesta al backend FarmaRAG.'}, {'flow_id': 'ayuda', 'score': np.float32(0.58746237), 'content': 'ayuda: Explicar las capacidades del asistente y los temas de auditoría farmacéutica que puede cubrir.'}, {'flow_id': 'fuera_tema', 'score': np.float32(0.57607), 'content': 'fuera tema: Responder de forma cortés cuando la consulta no pertenece al dominio de auditoría farmacéutica.'}] top_k=20
2026-05-05 14:15:33 DEBUG    rasa.dialogue_understanding.generator.llm_based_command_generator  - [debug    ] llm_based_command_generator.predict_commands.filtered_flows enabled_flow_retrieval=True message={'text': 'Jeffrey epstein esta vivo?', 'message_id': '5ed132b8cc2b47fbaeec377a49ef61e9', 'metadata': None, 'text_tokens': [<Token object value='Jeffrey' start=0 end=7         at 0x226fc62d310>, <Token object value='epstein' start=8 end=15         at 0x226fb8f2890>, <Token object value='esta' start=16 end=20         at 0x226fc4458d0>, <Token object value='vivo' start=21 end=25         at 0x226fc444c10>], 'intent': {'name': None, 'confidence': 0.0}, 'commands': [], 'flows_from_semantic_search': [('saludo', 0.6676324009895325), ('consulta_auditoria', 0.5896895527839661), ('ayuda', 0.5874623656272888), ('fuera_tema', 0.5760700106620789)], 'flows_in_prompt': ['consulta_auditoria', 'fuera_tema', 'saludo', 'ayuda']} relevant_flows=['consulta_auditoria', 'fuera_tema', 'saludo', 'ayuda']
2026-05-05 14:15:33 DEBUG    rasa.utils.log_utils  - [debug    ] llm_command_generator.predict_commands.prompt_rendered prompt='## Task
Analyze the conversation and output a list of actions (one per line). Below are examples of correct behaviour for slot extraction and for knowledge vs chitchat.

### Date & Time Context
- Current date: 05 May, 2026   (DD Month, YYYY)
- Current time: 17:15:33 (UTC)  (HH:MM:SS, 24-hour format with timezone)
- Current day: Tuesday     (Day of week)

---

## Examples (slot extraction and knowledge/chitchat)

**Slot extraction — extract every mentioned value:**
- User: "send money to John" → output must include a set slot for the recipient (e.g. `set slot recipient_account John`) and for transfer type if applicable, plus `start flow transfer_money`. Do not output only start flow when the user mentions a name or amount.
- User: "set up a recurrent payment" → output `start flow transfer_money`, `set slot transfer_type third party`, `set slot transfer_timing_type recurring` (all mentioned concepts must get a set slot).

**Knowledge vs chitchat:**
- User: "How do I change my PIN?" → `provide info` (concrete how-to question).
- User: "I\'m not sure how secure digitalization is." → `offtopic reply` (opinion/reflection, not a request for a factual answer).

---

## Available Flows and Slots
Use the following structured data:
```json
{"flows":[{"name":"saludo","description":"Saludar al usuario e iniciar la conversación de auditoría farmacéutica."},{"name":"consulta_auditoria","description":"Atender una consulta normativa o de auditoría farmacéutica delegando la respuesta al backend FarmaRAG."},{"name":"ayuda","description":"Explicar las capacidades del asistente y los temas de auditoría farmacéutica que puede cubrir."},{"name":"fuera_tema","description":"Responder de forma cortés cuando la consulta no pertenece al dominio de auditoría farmacéutica."}]}
```

---

## Available Actions
* `start flow flow_name`: Start a flow. E.g. `start flow transfer_money`, `start flow list_contacts`.
* `set slot slot_name slot_value`: Set a slot. E.g. `set slot transfer_money_recipient Freddy`. Output one set slot for every slot value the user mentions (names, amounts, types, etc.).
* `cancel flow`: Cancel the current flow when the user explicitly requests it.
* `disambiguate flows flow_name1 flow_name2 ...`: When user input is ambiguous, list possible flows. E.g. "contacts" → `disambiguate flows list_contacts add_contact remove_contact`.
* `provide info`: Answer FAQs, policies, service questions when no flow fits. Do not use for opinions or small talk.
* `offtopic reply`: Casual or social messages, opinions, general reflections.
* `hand over`: Hand over to a human when requested or when the user seems frustrated.
* `repeat message`: Repeat the last bot message.

---

## General instructions
* **Slot values:** Do not fill slots with placeholders or abstract values. For categorical slots, match the user message to allowed values or use "other". For boolean slots, map positive → `True`, negative → `False`. Extract text exactly as the user provided it.
* **Format:** Strictly adhere to the action format above. Focus on the last message; take it one step at a time. Use conversation history only to aid understanding.
* **Cancel / flows:** Do not cancel unless the user explicitly requests it. Multiple flows can be started without cancelling the previous one if the user pursues several things.
* Only use information provided by the user.

---

## Current State
Use the following structured data:
```json
{"active_flow":"pattern_completed","current_step":{"requested_slot":"continue_conversation","requested_slot_description":"Set this slot to `True` if the user needs further help and wants to continue the conversation. Set it to `False` otherwise."},"slots":[{"name":"continue_conversation","value":"undefined","type":"bool","description":"Set this slot to `True` if the user needs further help and wants to continue the conversation. Set it to `False` otherwise.","allowed_values":"[True, False]"}]}
```

---

## Conversation History
USER: Hola
AI: Hola. Puedo asistirle con consultas de auditoría farmacéutica. ¿Qué desea revisar?
AI: Is there anything else I can help you with?
USER: [User input triggered an error]
AI: Sorry, I am having trouble with that. Please try again in a few minutes.
AI: Is there anything else I can help you with?
USER: Jeffrey epstein esta vivo?

---

## Task
Create an action list with one action per line in response to the user\'s last message: """Jeffrey epstein esta vivo?""".

Your action list:'

Give Feedback / Get Help: https://github.com/BerriAI/litellm/issues/new
LiteLLM.Info: If you need to debug this error, use `litellm._turn_on_debug()'.

2026-05-05 14:15:33 ERROR    rasa.dialogue_understanding.generator.llm_based_command_generator  - [error    ] llm_based_command_generator.llm.error error=ProviderClientAPIException('
Original error: litellm.NotFoundError: GeminiException - )')
2026-05-05 14:15:33 WARNING  rasa.utils.log_utils  - [warning  ] ProviderClientAPIException occurred while predicting commands. commands=[ErrorCommand(error_type='rasa_internal_error_default', info={})] event_key=llm_command_generator.predict_commands.api_exception
2026-05-05 14:15:33 DEBUG    rasa.utils.log_utils  - [debug    ] 
=============================================================================================================================================================================
Commands predictd by the Command Generator
 commands=[ErrorCommand(error_type='rasa_internal_error_default', info={})] event_key=llm_command_generator.predict_commands.finished
=============================================================================================================================================================================
2026-05-05 14:15:33 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=RegexMessageHandler fn=process node_name=run_RegexMessageHandler
2026-05-05 14:15:33 DEBUG    rasa.core.processor  - [debug    ] processor.message.parse        parse_data_entities=[] parse_data_intent={'name': None, 'confidence': 0.0} parse_data_text='Jeffrey epstein esta vivo?'
2026-05-05 14:15:33 DEBUG    rasa.core.timer_stores.in_memory_timer_store  - [debug    ] timer_store.in_memory.timer_deleted sender_id=ad2a1a1e1edc41b6882b7d80757e1135
2026-05-05 14:15:33 DEBUG    rasa.core.timer_managers.in_memory_timer_manager  - [debug    ] timer_manager.in_memory.timer_cancelled sender_id=ad2a1a1e1edc41b6882b7d80757e1135
2026-05-05 14:15:33 DEBUG    rasa.core.timer_stores.in_memory_timer_store  - [debug    ] timer_store.in_memory.timer_stored scheduled_time=1778004933.5650423 sender_id=ad2a1a1e1edc41b6882b7d80757e1135 session_id=87ea532b-647e-46eb-8caf-c7d72ee18799
2026-05-05 14:15:33 DEBUG    rasa.core.timer_managers.in_memory_timer_manager  - [debug    ] timer_manager.in_memory.timer_scheduled sender_id=ad2a1a1e1edc41b6882b7d80757e1135 session_id=87ea532b-647e-46eb-8caf-c7d72ee18799 timeout_seconds=3600
2026-05-05 14:15:33 DEBUG    rasa.core.processor  - [debug    ] processor.session_timer.rescheduled sender_id=ad2a1a1e1edc41b6882b7d80757e1135 session_id=87ea532b-647e-46eb-8caf-c7d72ee18799 timeout_minutes=60
2026-05-05 14:15:33 DEBUG    rasa.core.processor  - [debug    ] Logged UserUtterance.          event_key=rasa.core.processor.handle_message_with_tracker number_of_events=49 user_message='Jeffrey epstein esta vivo?'
2026-05-05 14:15:33 DEBUG    rasa.engine.runner.dask  - [debug    ] Running graph with inputs, targets and execution context. event_key=rasa.engine.runner.dask.run execution_context=ExecutionContext(model_id='a076f846c70a4d269ab37f3809ece1d8', should_add_diagnostic_data=False, is_finetuning=False, node_name=None) inputs={} targets=['flows_provider']
2026-05-05 14:15:33 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-05-05 14:15:33 DEBUG    rasa.core.processor  - [debug    ] processor.extract.slots        action_extract_slot=action_extract_slots len_extraction_events=0 rasa_events=[]
2026-05-05 14:15:33 DEBUG    rasa.engine.runner.dask  - [debug    ] Running graph with inputs, targets and execution context. event_key=rasa.engine.runner.dask.run execution_context=ExecutionContext(model_id='a076f846c70a4d269ab37f3809ece1d8', should_add_diagnostic_data=False, is_finetuning=False, node_name=None) inputs={'__tracker__': DialogueStateTracker(sender_id: ad2a1a1e1edc41b6882b7d80757e1135)} targets=['command_processor']
2026-05-05 14:15:33 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-05-05 14:15:33 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DomainProvider fn=provide_inference node_name=domain_provider
2026-05-05 14:15:33 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=CommandProcessorComponent fn=execute_commands node_name=command_processor
2026-05-05 14:15:33 DEBUG    rasa.dialogue_understanding.processor.command_processor  - [debug    ] 
=============================================================================================================================================================================
Final commands
 command=[ErrorCommand(error_type='rasa_internal_error_default', info={})] event_key=command_processor.clean_up_commands.final_commands
=============================================================================================================================================================================
2026-05-05 14:15:33 DEBUG    rasa.dialogue_understanding.commands.error_command  - [debug    ] error_command.error            command=ErrorCommand(error_type='rasa_internal_error_default', info={})
2026-05-05 14:15:33 DEBUG    rasa.engine.runner.dask  - [debug    ] Running graph with inputs, targets and execution context. event_key=rasa.engine.runner.dask.run execution_context=ExecutionContext(model_id='a076f846c70a4d269ab37f3809ece1d8', should_add_diagnostic_data=False, is_finetuning=False, node_name=None) inputs={'__tracker__': DialogueStateTracker(sender_id: ad2a1a1e1edc41b6882b7d80757e1135), '__endpoints__': <rasa.core.config.available_endpoints.AvailableEndpoints object at 0x00000226CA139710>, '__output_channel__': <rasa.core.channels.rest.QueueOutputChannel object at 0x00000226FBBB8550>, '__cancellation_token__': <rasa.agents.core.cancellation.CancellationToken object at 0x00000226FBBB9E90>} targets=['select_prediction']
2026-05-05 14:15:33 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=RuleOnlyDataProvider fn=provide node_name=rule_only_data_provider
2026-05-05 14:15:33 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DomainProvider fn=provide_inference node_name=domain_provider
2026-05-05 14:15:33 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-05-05 14:15:33 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowPolicy fn=predict_action_probabilities node_name=run_FlowPolicy0
2026-05-05 14:15:33 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_internal_error previous_step_id=START
2026-05-05 14:15:33 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=START flow_id=pattern_internal_error next_id=pattern_internal_error_0_noop
2026-05-05 14:15:33 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.no_operation     flow_id=pattern_internal_error step_id=pattern_internal_error_0_noop
2026-05-05 14:15:33 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_internal_error previous_step_id=pattern_internal_error_0_noop
2026-05-05 14:15:33 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.predicate.evaluating      condition='context.error_type is "rasa_internal_error_user_input_too_long"' flow_id=pattern_internal_error rendered_condition='context.error_type is "rasa_internal_error_user_input_too_long"'
2026-05-05 14:15:33 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.predicate.evaluating      condition='context.error_type is "rasa_internal_error_user_input_empty"' flow_id=pattern_internal_error rendered_condition='context.error_type is "rasa_internal_error_user_input_empty"'
2026-05-05 14:15:33 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.link.else_condition_satisfied current_id=pattern_internal_error_0_noop flow_id=pattern_internal_error target=pattern_internal_error_3_utter_internal_error_rasa
2026-05-05 14:15:33 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=pattern_internal_error_0_noop flow_id=pattern_internal_error next_id=pattern_internal_error_3_utter_internal_error_rasa
2026-05-05 14:15:33 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.action           context={'context': {'frame_id': '811SQO1M', 'flow_id': 'pattern_internal_error', 'step_id': 'pattern_internal_error_3_utter_internal_error_rasa', 'error_type': 'rasa_internal_error_default', 'info': {}, 'type': 'pattern_internal_error'}} flow_id=pattern_internal_error step_id=pattern_internal_error_3_utter_internal_error_rasa
2026-05-05 14:15:33 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DefaultPolicyPredictionEnsemble fn=combine_predictions_from_kwargs node_name=select_prediction
2026-05-05 14:15:33 DEBUG    rasa.core.policies.ensemble  - Made prediction using user intent.
2026-05-05 14:15:33 DEBUG    rasa.core.policies.ensemble  - Added `DefinePrevUserUtteredFeaturization(False)` event.
2026-05-05 14:15:33 DEBUG    rasa.core.policies.ensemble  - Predicted next action using FlowPolicy.
2026-05-05 14:15:33 DEBUG    rasa.core.processor  - [debug    ] Predicted next action.         action=utter_internal_error_rasa confidence=1.0 event_key=rasa.core.processor.predict_next_with_tracker_if_should
2026-05-05 14:15:33 DEBUG    rasa.core.processor  - [debug    ] processor.actions.policy_prediction action_name=utter_internal_error_rasa policy_name=FlowPolicy prediction_events=[DialogueStackUpdate("""[{"op": "replace", "path": "/2/step_id", "value": "pattern_internal_error_0_noop"}]"""), FlowStarted(flow: pattern_internal_error), DialogueStackUpdate("""[{"op": "replace", "path": "/2/step_id", "value": "pattern_internal_error_3_utter_internal_error_rasa"}]"""), <rasa.shared.core.events.DefinePrevUserUtteredFeaturization object at 0x00000226FC446550>]
2026-05-05 14:15:33 DEBUG    rasa.core.processor  - [debug    ] processor.actions.log          action_name=utter_internal_error_rasa rasa_events=[BotUttered('Sorry, I am having trouble with that. Please try again in a few minutes.', {"elements": null, "quick_replies": null, "buttons": null, "attachment": null, "image": null, "custom": null}, {"active_flow": "pattern_internal_error", "step_id": "pattern_internal_error_3_utter_internal_error_rasa", "utter_action": "utter_internal_error_rasa", "utter_source": "TemplatedNaturalLanguageGenerator"}, 1778001333.6856115)]
2026-05-05 14:15:33 DEBUG    rasa.engine.runner.dask  - [debug    ] Running graph with inputs, targets and execution context. event_key=rasa.engine.runner.dask.run execution_context=ExecutionContext(model_id='a076f846c70a4d269ab37f3809ece1d8', should_add_diagnostic_data=False, is_finetuning=False, node_name=None) inputs={'__tracker__': DialogueStateTracker(sender_id: ad2a1a1e1edc41b6882b7d80757e1135), '__endpoints__': <rasa.core.config.available_endpoints.AvailableEndpoints object at 0x00000226CA139710>, '__output_channel__': <rasa.core.channels.rest.QueueOutputChannel object at 0x00000226FBBB8550>, '__cancellation_token__': <rasa.agents.core.cancellation.CancellationToken object at 0x00000226FBBB9E90>} targets=['select_prediction']
2026-05-05 14:15:33 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=RuleOnlyDataProvider fn=provide node_name=rule_only_data_provider
2026-05-05 14:15:33 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DomainProvider fn=provide_inference node_name=domain_provider
2026-05-05 14:15:33 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-05-05 14:15:33 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowPolicy fn=predict_action_probabilities node_name=run_FlowPolicy0
2026-05-05 14:15:33 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_internal_error previous_step_id=pattern_internal_error_3_utter_internal_error_rasa
2026-05-05 14:15:33 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=pattern_internal_error_3_utter_internal_error_rasa flow_id=pattern_internal_error next_id=END
2026-05-05 14:15:33 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.flow_end         flow_id=pattern_internal_error step_id=END
2026-05-05 14:15:33 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_collect_information previous_step_id=pattern_collect_information_4_action_listen
2026-05-05 14:15:33 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=pattern_collect_information_4_action_listen flow_id=pattern_collect_information next_id=start
2026-05-05 14:15:33 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.action           context={'context': {'frame_id': 'MFCKSIFB', 'flow_id': 'pattern_completed', 'step_id': 'pattern_completed_0_collect_continue_conversation', 'collect': 'continue_conversation', 'utter': 'utter_ask_continue_conversation', 'collect_action': 'action_ask_continue_conversation', 'rejections': [], 'type': 'pattern_completed', 'previous_flow_name': 'saludo'}} flow_id=pattern_collect_information step_id=start
2026-05-05 14:15:33 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DefaultPolicyPredictionEnsemble fn=combine_predictions_from_kwargs node_name=select_prediction
2026-05-05 14:15:33 DEBUG    rasa.core.policies.ensemble  - Predicted next action using FlowPolicy.
2026-05-05 14:15:33 DEBUG    rasa.core.processor  - [debug    ] Predicted next action.         action=action_run_slot_rejections confidence=1.0 event_key=rasa.core.processor.predict_next_with_tracker_if_should
2026-05-05 14:15:33 DEBUG    rasa.core.processor  - [debug    ] processor.actions.policy_prediction action_name=action_run_slot_rejections policy_name=FlowPolicy prediction_events=[DialogueStackUpdate("""[{"op": "replace", "path": "/2/step_id", "value": "END"}]"""), DialogueStackUpdate("""[{"op": "remove", "path": "/2"}]"""), FlowCompleted(flow: pattern_internal_error, step_id: pattern_internal_error_3_utter_internal_error_rasa), DialogueStackUpdate("""[{"op": "replace", "path": "/1/step_id", "value": "start"}]""")]
2026-05-05 14:15:33 DEBUG    rasa.core.processor  - [debug    ] processor.actions.log          action_name=action_run_slot_rejections rasa_events=[]
2026-05-05 14:15:33 DEBUG    rasa.core.processor  - [debug    ] processor.slots.user_slots     slots={'language': 'es', 'max_clarification_options': 3.0, 'fallback_triggered': False}
2026-05-05 14:15:33 DEBUG    rasa.engine.runner.dask  - [debug    ] Running graph with inputs, targets and execution context. event_key=rasa.engine.runner.dask.run execution_context=ExecutionContext(model_id='a076f846c70a4d269ab37f3809ece1d8', should_add_diagnostic_data=False, is_finetuning=False, node_name=None) inputs={'__tracker__': DialogueStateTracker(sender_id: ad2a1a1e1edc41b6882b7d80757e1135), '__endpoints__': <rasa.core.config.available_endpoints.AvailableEndpoints object at 0x00000226CA139710>, '__output_channel__': <rasa.core.channels.rest.QueueOutputChannel object at 0x00000226FBBB8550>, '__cancellation_token__': <rasa.agents.core.cancellation.CancellationToken object at 0x00000226FBBB9E90>} targets=['select_prediction']
2026-05-05 14:15:33 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=RuleOnlyDataProvider fn=provide node_name=rule_only_data_provider
2026-05-05 14:15:33 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DomainProvider fn=provide_inference node_name=domain_provider
2026-05-05 14:15:33 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-05-05 14:15:33 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowPolicy fn=predict_action_probabilities node_name=run_FlowPolicy0
2026-05-05 14:15:33 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_collect_information previous_step_id=start
2026-05-05 14:15:33 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=start flow_id=pattern_collect_information next_id=pattern_collect_information_1_validate_{{context.collect}}
2026-05-05 14:15:33 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_collect_information previous_step_id=pattern_collect_information_1_validate_{{context.collect}}
2026-05-05 14:15:33 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.predicate.evaluating      condition='slots.{{context.collect}} is not null' flow_id=pattern_collect_information rendered_condition='slots.continue_conversation is not null'
2026-05-05 14:15:33 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.link.else_condition_satisfied current_id=pattern_collect_information_1_validate_{{context.collect}} flow_id=pattern_collect_information target=ask_collect
2026-05-05 14:15:33 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=pattern_collect_information_1_validate_{{context.collect}} flow_id=pattern_collect_information next_id=ask_collect
2026-05-05 14:15:33 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.action           context={'context': {'frame_id': 'MFCKSIFB', 'flow_id': 'pattern_completed', 'step_id': 'pattern_completed_0_collect_continue_conversation', 'collect': 'continue_conversation', 'utter': 'utter_ask_continue_conversation', 'collect_action': 'action_ask_continue_conversation', 'rejections': [], 'type': 'pattern_completed', 'previous_flow_name': 'saludo'}} flow_id=pattern_collect_information step_id=ask_collect
2026-05-05 14:15:33 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DefaultPolicyPredictionEnsemble fn=combine_predictions_from_kwargs node_name=select_prediction
2026-05-05 14:15:33 DEBUG    rasa.core.policies.ensemble  - Predicted next action using FlowPolicy.
2026-05-05 14:15:33 DEBUG    rasa.core.processor  - [debug    ] Predicted next action.         action=utter_ask_continue_conversation confidence=1.0 event_key=rasa.core.processor.predict_next_with_tracker_if_should
2026-05-05 14:15:33 DEBUG    rasa.core.processor  - [debug    ] processor.actions.policy_prediction action_name=utter_ask_continue_conversation policy_name=FlowPolicy prediction_events=[DialogueStackUpdate("""[{"op": "replace", "path": "/1/step_id", "value": "pattern_collect_information_1_validate_{{context.collect}}"}]"""), DialogueStackUpdate("""[{"op": "replace", "path": "/1/step_id", "value": "ask_collect"}]""")]
2026-05-05 14:15:33 DEBUG    rasa.core.processor  - [debug    ] processor.actions.log          action_name=utter_ask_continue_conversation rasa_events=[BotUttered('Is there anything else I can help you with?', {"elements": null, "quick_replies": null, "buttons": null, "attachment": null, "image": null, "custom": null}, {"metadata": {"rephrase": true}, "active_flow": "pattern_completed", "step_id": "pattern_completed_0_collect_continue_conversation", "utter_action": "utter_ask_continue_conversation", "utter_source": "TemplatedNaturalLanguageGenerator"}, 1778001333.7813437)]
2026-05-05 14:15:33 DEBUG    rasa.engine.runner.dask  - [debug    ] Running graph with inputs, targets and execution context. event_key=rasa.engine.runner.dask.run execution_context=ExecutionContext(model_id='a076f846c70a4d269ab37f3809ece1d8', should_add_diagnostic_data=False, is_finetuning=False, node_name=None) inputs={'__tracker__': DialogueStateTracker(sender_id: ad2a1a1e1edc41b6882b7d80757e1135), '__endpoints__': <rasa.core.config.available_endpoints.AvailableEndpoints object at 0x00000226CA139710>, '__output_channel__': <rasa.core.channels.rest.QueueOutputChannel object at 0x00000226FBBB8550>, '__cancellation_token__': <rasa.agents.core.cancellation.CancellationToken object at 0x00000226FBBB9E90>} targets=['select_prediction']
2026-05-05 14:15:33 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=RuleOnlyDataProvider fn=provide node_name=rule_only_data_provider
2026-05-05 14:15:33 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DomainProvider fn=provide_inference node_name=domain_provider
2026-05-05 14:15:33 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-05-05 14:15:33 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowPolicy fn=predict_action_probabilities node_name=run_FlowPolicy0
2026-05-05 14:15:33 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_collect_information previous_step_id=ask_collect
2026-05-05 14:15:33 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=ask_collect flow_id=pattern_collect_information next_id=pattern_collect_information_3_{{context.collect_action}}
2026-05-05 14:15:33 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_collect_information previous_step_id=pattern_collect_information_3_{{context.collect_action}}
2026-05-05 14:15:33 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=pattern_collect_information_3_{{context.collect_action}} flow_id=pattern_collect_information next_id=pattern_collect_information_4_action_listen
2026-05-05 14:15:33 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.action           context={'context': {'frame_id': 'MFCKSIFB', 'flow_id': 'pattern_completed', 'step_id': 'pattern_completed_0_collect_continue_conversation', 'collect': 'continue_conversation', 'utter': 'utter_ask_continue_conversation', 'collect_action': 'action_ask_continue_conversation', 'rejections': [], 'type': 'pattern_completed', 'previous_flow_name': 'saludo'}} flow_id=pattern_collect_information step_id=pattern_collect_information_4_action_listen
Sorry, I am having trouble with that. Please try again in a few minutes.
2026-05-05 14:15:33 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DefaultPolicyPredictionEnsemble fn=combine_predictions_from_kwargs node_name=select_prediction
2026-05-05 14:15:33 DEBUG    rasa.core.policies.ensemble  - Predicted next action using FlowPolicy.
2026-05-05 14:15:33 DEBUG    rasa.core.processor  - [debug    ] Predicted next action.         action=action_listen confidence=1.0 event_key=rasa.core.processor.predict_next_with_tracker_if_should
2026-05-05 14:15:33 DEBUG    rasa.core.processor  - [debug    ] processor.actions.policy_prediction action_name=action_listen policy_name=FlowPolicy prediction_events=[DialogueStackUpdate("""[{"op": "replace", "path": "/1/step_id", "value": "pattern_collect_information_3_{{context.collect_action}}"}]"""), DialogueStackUpdate("""[{"op": "replace", "path": "/1/step_id", "value": "pattern_collect_information_4_action_listen"}]""")]
2026-05-05 14:15:33 DEBUG    rasa.core.processor  - [debug    ] processor.actions.log          action_name=action_listen rasa_events=[]
2026-05-05 14:15:33 DEBUG    rasa.core.tracker_stores.tracker_store  - [debug    ] No event broker configured. Skipping streaming events. event_key=tracker_store.stream_events.no_broker_configured
2026-05-05 14:15:33 DEBUG    rasa.core.processor  - [debug    ] processor.trigger_anonymization.skipping.pii_management_not_enabled
2026-05-05 14:15:33 DEBUG    rasa.core.lock_store  - [debug    ] Deleted lock for conversation 'ad2a1a1e1edc41b6882b7d80757e1135'. event_key=lock_store._deleted_lock_for_conversation
Is there anything else I can help you with?