StepAgendaComponent = {
    props: [],
    data() {
        return {
            agendas: JSON.parse(document.getElementById('agendas_json').textContent),
            themes: JSON.parse(document.getElementById('themes_json').textContent),
            theme: '',
        }
    },
    template: `
        <div class="mb-3 input-group">
            <textarea name="theme" id="theme-field" class="form-control" v-model="theme" placeholder="Тема выступления" title=""></textarea>
            <button type="button" @click="save_theme" class="btn btn-secondary"> >>> </button>
        </div>
        <div v-for="theme in themes">
						<div style="background-color: var(--bs-card-border-color); padding: 5px; border-radius: 3px; display: flex; justify-content: space-between;">
								<span>[[ theme.duration ]] мин</span>
								<span>[[ theme.theme ]]</span>
								<span>[[ theme.username ]]</span>
						</div>
						<br>
        </div>

        <template v-for="agenda in agendas">
            <step-agenda-self-item-component
                v-if="agenda.self"
                :invited="agenda.invited"
                :themes="agenda.themes"
                :themes_duration="agenda.themes_duration"
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
                    :themes="agenda.themes"
                    :themes_duration="agenda.themes_duration"
                    :questions="agenda.questions"
                    :fundamental_objections="agenda.fundamental_objections"
                    :suggested_solutions="agenda.suggested_solutions"
                    :counter_offer="agenda.counter_offer"
                ></step-agenda-item-component>
            </div>
        </template>
    `,
    methods: {
        save_agenda(component, event) {
            $.ajax({
                url: URL_FACI_EDITOR_AGENDA,
                headers: {
                    "X-CSRFToken": CSRF_TOKEN,
                },
                dataType: 'json',
                data: {
                    themes: component.m_themes,
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
        save_theme(event) {
            let self = this;
            if (!self.theme) return;
            $.ajax({
                url: URL_FACI_ADD_THEME,
                headers: {
                    "X-CSRFToken": CSRF_TOKEN,
                },
                dataType: 'json',
                data: {'theme': self.theme, duration: 5},
                success: function(result) {
                    set_valid_field(event.target.form, result.updated);
                    self.themes.unshift({username: CURRENT_USERNAME, duration: 5, theme: self.theme});
                    self.theme = '';
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
