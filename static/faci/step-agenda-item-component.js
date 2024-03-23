const StepAgendaItemComponent = {
		props: [
				'invited',
				//'themes',
				//'themes_duration',
				'questions',
				'fundamental_objections',
				'suggested_solutions',
				'counter_offer',
		],
		emits: [],
		template: `
				<!--<div style="background-color: var(--bs-card-border-color); padding: 5px; border-radius: 3px; display: flex; justify-content: space-between;">
						<span>[[ themes_duration ]] мин</span>
						<span>[[ invited ]]</span>
				</div>-->

				<br>

				<!--<div v-if="themes">
						<div style="font-style: italic;">Тема выступления участника:</div>
						<p style="padding-left: 15px;"><pre>[[ themes ]]</pre></p>
				</div>-->

				<div v-if="questions">
						<div style="font-style: italic;">Вопросы:</div>
						<p style="padding-left: 15px;"><pre style="font: inherit;">[[ questions ]]</pre></p>
				</div>

				<div v-if="fundamental_objections">
						<div style="font-style: italic;">Принципиальные возражения:</div>
						<p style="padding-left: 15px;"><pre style="font: inherit;">[[ fundamental_objections ]]</pre></p>
				</div>

				<div v-if="suggested_solutions">
						<div style="font-style: italic;">Предлагаемые решения:</div>
						<p style="padding-left: 15px;"><pre style="font: inherit;">[[ suggested_solutions ]]</pre></p>
				</div>

				<div v-if="counter_offer">
						<div style="font-style: italic;">Встречные предложения:</div>
						<p style="padding-left: 15px;"><pre style="font: inherit;">[[ counter_offer ]]</pre></p>
				</div>
				`,
};
