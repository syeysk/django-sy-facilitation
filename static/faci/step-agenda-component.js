StepAgendaComponent = {
    data() {
        return {
            expr_types: JSON.parse(document.getElementById('expr_types_json').textContent),
            theme: '',
            duration: '',
            description: '',
            current_theme_id: null,
            current_expression_type: null,
            expressions: [],
            expression: '',
            HAS_ACCESS_TO_ADD_EXPRESSION,
            HAS_ACCESS_TO_ADD_THEME,
            MEETING_STATUS_EDITING,
        }
    },
    template: `
        <div v-if="HAS_ACCESS_TO_ADD_THEME && faci.meeting_status == MEETING_STATUS_EDITING">
						<textarea name="theme" id="theme-field" class="form-control" v-model="theme" placeholder="Тема выступления" title=""></textarea>
						<textarea name="description" id="theme-field" class="form-control" v-model="description" placeholder="Расскажите подробнее" title=""></textarea>

						<div class="mb-3 input-group">
								<input @keyup.enter="add_theme" name="duration" id="duration-field" type="number" class="form-control" v-model="duration" placeholder="Длительность выступления, мин." title="длительность выступления для темы, в минутах">
								<button type="button" @click="add_theme" class="btn btn-outline-primary" @submit.prevent> >>> </button>
						</div>
			  </div>

        <div v-for="theme in themes" class="theme">
						<div class="theme-header" :data-id="theme.id.toString()" :key="theme.id" @click="open_theme" style="padding: 5px; cursor: pointer;">
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
						    <p v-if="theme.description"><pre style="font: inherit">[[ theme.description ]]</pre></p>
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
												<div class="mb-3 input-group" v-if="HAS_ACCESS_TO_ADD_EXPRESSION && faci.meeting_status == MEETING_STATUS_EDITING">
														<input name="expression" id="expression-field" class="form-control" v-model="expression" :placeholder="expr_type[1]" @keyup.enter="add_expression" type="text">
														<button type="button" @click="add_expression" class="btn btn-outline-primary"> >>> </button>
												</div>
										</div>
							  </div>
						</div>
        </div>
    `,
    inject: ['themes', 'faci'],
    methods: {
        open_expressions(event) {
            let header_el = event.target.closest('.counter-header')
            if (this.current_expression_type == header_el.dataset.counter) {
                this.current_expression_type = null;
                this.expressions = [];
            } else {
                this.current_expression_type = header_el.dataset.counter;
                this.get_expressions();
            }
        },
        open_theme(event) {
            let header_el = event.target.closest('.theme-header')
            if (this.current_theme_id == header_el.dataset.id) {
                this.current_theme_id = null;
            } else {
                this.current_theme_id = header_el.dataset.id;
            }
            this.current_expression_type = null;
            this.expressions = [];
        },
        add_theme(event) {
            let self = this;
            if (!self.theme) return;
            $.ajax({
                url: URL_FACI_EDITOR_ADD_THEME,
                headers: {"X-CSRFToken": CSRF_TOKEN},
                dataType: 'json',
                data: {theme: self.theme, duration: self.duration, description: self.description},
                success: function(result) {
                    set_valid_field(event.target.form, result.updated);
                    self.themes.unshift(
                        {username: CURRENT_USERNAME, duration: self.duration, theme: self.theme, id: result.id.toString(), description: self.description},
                    );
                    self.theme = '';
                    self.duration = '';
                    self.description = '';
                    self.faci.step = result.step;
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
}
