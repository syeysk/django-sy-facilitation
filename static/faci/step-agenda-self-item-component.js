const StepAgendaSelfItemComponent = {
    props: [
        'invited',
        'themes',
        'themes_duration',
        'questions',
        'fundamental_objections',
        'suggested_solutions',
        'counter_offer',
    ],
    emits: ['click'],
    data() {
        return {
            m_themes: this.themes,
            m_themes_duration: this.themes_duration,
            m_questions: this.questions,
            m_fundamental_objections: this.fundamental_objections,
            m_suggested_solutions: this.suggested_solutions,
            m_counter_offer: this.counter_offer,
        };
    },
    template: `
        <div style="background-color: var(--bs-card-border-color); padding: 5px; border-radius: 3px; display: flex; justify-content: space-between;">
            <span>
                <div class="mb-3 form-group" id="themes_duration-group" style="display: inline-block; margin-bottom: 0 !important;">
                    <input v-model="m_themes_duration" name="themes_duration" min="1" max="120" type="number" style="width: 45pt; padding: 0 0 0 3px; display: initial;" class="form-control" id="themes_duration-field">
                </div> мин
            </span>
            <span>[[ invited ]]</span>
        </div>

        <br>

        <div class="mb-3 form-group" id="themes-group">
            <div class="form-floating">
                <textarea v-model="m_themes" name="themes" style="width: 100%; height: 100px;" class="form-control" id="themes-field"></textarea>
                <label for="themes-field" class="form-label">Тема выступления участника:</label>
            </div>
        </div>

        <div class="mb-3 form-group" id="questions-group">
            <div class="form-floating">
                <textarea v-model="m_questions" name="questions" style="width: 100%; height: 100px;" class="form-control" id="questions-field"></textarea>
                <label for="questions-field" class="form-label">Вопросы:</label>
            </div>
        </div>

        <div class="mb-3 form-group" id="fundamental_objections-group">
            <div class="form-floating">
                <textarea v-model="m_fundamental_objections" name="fundamental_objections" style="width: 100%; height: 100px;" class="form-control" id="fundamental_objections-field"></textarea>
                <label for="fundamental_objections-field" class="form-label">Принципиальные возражения:</label>
            </div>
        </div>

        <div class="mb-3 form-group" id="suggested_solutions-group">
            <div class="form-floating">
                <textarea v-model="m_suggested_solutions" name="suggested_solutions" style="width: 100%; height: 100px;" class="form-control" id="suggested_solutions-field"></textarea>
                <label for="suggested_solutions-field" class="form-label">Предлагаемые решения:</label>
            </div>
        </div>

        <div class="mb-3 form-group" id="counter_offer-group">
            <div class="form-floating">
                <textarea v-model="m_counter_offer" name="counter_offer" style="width: 100%; height: 100px;" class="form-control" id="counter_offer-field"></textarea>
                <label for="counter_offer-field" class="form-label">Встречные предложения:</label>
            </div>
        </div>

        <input type="button" value="Сохранить" class="btn btn-secondary" @click="click">

        <br>
        `,
    methods: {
        click(event) {
            this.$emit('click', this, event);
        },
    },
};
