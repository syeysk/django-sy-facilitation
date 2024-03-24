StepAgendaComponent = {
    props: [],
    data() {
        return {
            agendas: JSON.parse(document.getElementById('agendas_json').textContent),
            expr_types: JSON.parse(document.getElementById('expr_types_json').textContent),
            themes,
            theme: '',
            duration: '',
            current_theme_id: null,
            current_expression_type: null,
            expressions: [],
            expression: '',
        }
    },
    template: `
        <div class="mb-3 input-group">
            <span class="form-control" style="padding: 0; border: none;">
                <input name="duration" id="duration-field" class="form-control" v-model="duration" placeholder="Длительность, мин." title="длительность выступления для темы, в минутах">
                <textarea name="theme" id="theme-field" class="form-control" v-model="theme" placeholder="Тема выступления" title=""></textarea>
            </span>
            <button type="button" @click="add_theme" class="btn btn-secondary"> >>> </button>
        </div>

        <div v-for="theme in themes">
						<div class="theme-header" :data-id="theme.id.toString()" :key="theme.id" @click="open_theme" style="padding: 5px; cursor: pointer; border-bottom: 1px solid #c1c1c1;">
								<div style="display: flex; justify-content: space-between;">
    								<span :style="current_theme_id == theme.id.toString() ? 'font-weight: 600;' : 'font-weight: inherit;'">[[ theme.theme ]]</span>
    								<span v-if="current_theme_id == theme.id.toString()">-</span>
    								<span v-else>+</span>
							  </div>
								<div style="display: flex; justify-content: space-between; font-size: 10pt; color: grey;">
										<span>[[ theme.duration ]] мин</span>
										<span>[[ theme.username ]]</span>
							  </div>
						</div>

						<div v-if="current_theme_id == theme.id.toString()" style="padding-left: 15px;">
						    <div v-for="expr_type in expr_types">
										<div :data-counter="expr_type[0].toString()" class="counter-header" @click="open_expressions" style="cursor: pointer; padding: 5px 0;">
												<span v-if="current_expression_type == expr_type[0].toString()">- </span>
												<span v-else>+</span>
												[[ expr_type[1] ]]
										</div>
										<div v-if="current_expression_type == expr_type[0].toString()" style="padding-left: 1rem;">
												<p v-for="expression in expressions" style="font-size: 10pt;">
												    <b>[[ expression.username ]]:</b> [[ expression.expression ]]
												</p>
												<div class="mb-3 input-group">
														<textarea name="expression" id="expression-field" class="form-control" style="height: 80px; font-size: 10pt;"  v-model="expression" :placeholder="expr_type[1]"></textarea>
														<button type="button" @click="add_expression" class="btn btn-secondary"> >>> </button>
												</div>
										</div>
							  </div>
						</div>
						<br>
        </div>

        <!--<template v-for="agenda in agendas">
            <step-agenda-self-item-component
                v-if="agenda.self"
                :invited="agenda.invited"
                :questions="agenda.questions"
                :fundamental_objections="agenda.fundamental_objections"
                :suggested_solutions="agenda.suggested_solutions"
                :counter_offer="agenda.counter_offer"
                @click="save_agenda"
            ></step-agenda-self-item-component>
            <div
                v-else
            >
                <step-agenda-item-component
                    v-if="agenda.themes || agenda.questions"
                    :invited="agenda.invited"
                    :questions="agenda.questions"
                    :fundamental_objections="agenda.fundamental_objections"
                    :suggested_solutions="agenda.suggested_solutions"
                    :counter_offer="agenda.counter_offer"
                ></step-agenda-item-component>
            </div>
        </template>-->
    `,
    methods: {
        open_expressions(event) {
            let header_el = event.target.closest('.counter-header')
            if (this.current_expression_type == header_el.dataset.counter) {
                this.current_expression_type = null;
            } else {
                this.current_expression_type = header_el.dataset.counter;
            }
            this.get_expressions();
        },
        open_theme(event) {
            let header_el = event.target.closest('.theme-header')
            if (this.current_theme_id == header_el.dataset.id) {
                this.current_theme_id = null;
            } else {
                this.current_theme_id = header_el.dataset.id;
            }
        },
        save_agenda(component, event) {
            $.ajax({
                url: URL_FACI_EDITOR_AGENDA,
                headers: {"X-CSRFToken": CSRF_TOKEN},
                dataType: 'json',
                data: {
                    //themes: component.m_themes,
                    themes_duration: component.m_themes_duration,
                    questions: component.m_questions,
                    fundamental_objections: component.m_fundamental_objections,
                    suggested_solutions: component.m_suggested_solutions,
                    counter_offer: component.m_counter_offer,
                },
                success: function(result) {
                    set_valid_field(event.target.form, result.updated);
                    open_block(result['open_block']);
                },
                error: function(jqxhr, a, b) {
                    console.log('error');
                },
                statusCode: {
                    403: function(xhr) {
                        alert(xhr.responseJSON.detail);
                    },
                    400: function(xhr) {
                        set_invalid_field(event.target.form, xhr.responseJSON);
                    },
                },
                method: "post"
            });
        },
        add_theme(event) {
            let self = this;
            if (!self.theme) return;
            $.ajax({
                url: URL_FACI_EDITOR_ADD_THEME,
                headers: {"X-CSRFToken": CSRF_TOKEN},
                dataType: 'json',
                data: {'theme': self.theme, duration: self.duration},
                success: function(result) {
                    set_valid_field(event.target.form, result.updated);
                    self.themes.unshift(
                        {username: CURRENT_USERNAME, duration: self.duration, theme: self.theme, id: result.id.toString()},
                    );
                    self.theme = '';
                    self.duration = '';
                },
                statusCode: {
                    403: function(xhr) {
                        alert(xhr.responseJSON.detail);
                    },
                    400: function(xhr) {
                        set_invalid_field(event.target.form, xhr.responseJSON);
                    },
                },
                method: "post"
            });
        },
        add_expression(event) {
            let self = this;
            if (!self.expression) return;
            $.ajax({
                url: URL_FACI_EDITOR_ADD_EXPRESSION,
                headers: {
                    "X-CSRFToken": CSRF_TOKEN,
                },
                dataType: 'json',
                data: {expression: self.expression, theme: self.current_theme_id, expression_type: self.current_expression_type},
                success: function(result) {
                    set_valid_field(event.target.form, result.updated);
                    self.expressions.push({username: CURRENT_USERNAME, expression: self.expression})
                    self.expression = '';
                },
                statusCode: {
                    403: function(xhr) {
                        alert(xhr.responseJSON.detail);
                    },
                    400: function(xhr) {
                        set_invalid_field(event.target.form, xhr.responseJSON);
                    },
                },
                method: "post"
            });
        },
        get_expressions() {
            let self = this;
            $.ajax({
                url: URL_FACI_EDITOR_GET_EXPRESSIONS,
                headers: {"X-CSRFToken": CSRF_TOKEN},
                dataType: 'json',
                data: {theme: self.current_theme_id, expression_type: self.current_expression_type},
                success: function(result) {
                    self.expressions = result.expressions;
                },
                statusCode: {
                    403: function(xhr) {
                        alert(xhr.responseJSON.detail);
                    },
                },
                method: "post"
            });
        },
    },
    components: {StepAgendaItemComponent, StepAgendaSelfItemComponent},
}
