StepAgendaComponent = {
    props: [],
    data() {
        return {
            agendas: JSON.parse(document.getElementById('agendas_json').textContent),
            themes,
            theme: '',
            duration: '',
            current_theme_id: null,
            current_counter: null,
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
						    <div data-counter="questions" class="counter-header" @click="open_counter">
    						    Вопросы
						    </div>
    						<div v-if="current_counter == 'questions'">
    						    В разработке...
    						</div>

						    <div data-counter="fundamental_objections" class="counter-header" @click="open_counter">
                    Принципиальные возражения
						    </div>
						    <div v-if="current_counter == 'fundamental_objections'">
						        В разработке...
						    </div>

						    <div data-counter="suggested_solutions" class="counter-header" @click="open_counter">
						        Предлагаемые решения
						    </div>
						    <div v-if="current_counter == 'suggested_solutions'">
						        В разработке...
						    </div>

						    <div data-counter="counter_offer" class="counter-header" @click="open_counter">
						        Встречные предложения
						    </div>
						    <div v-if="current_counter == 'counter_offer'">
						        В разработке...
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
        open_counter(event) {
            let header_el = event.target.closest('.counter-header')
            if (this.current_counter == header_el.dataset.counter) {
                this.current_counter = null;
            } else {
                this.current_counter = header_el.dataset.counter;
            }
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
                headers: {
                    "X-CSRFToken": CSRF_TOKEN,
                },
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
                headers: {
                    "X-CSRFToken": CSRF_TOKEN,
                },
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
    },
    components: {StepAgendaItemComponent, StepAgendaSelfItemComponent},
}
