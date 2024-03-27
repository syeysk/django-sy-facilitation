StepKeyThoughtsComponent = {
    data() {
        return {
            sent_parked_thought: '',
            parked_thought: '',
            HAS_ACCESS_TO_ADD_PARKED_THOUGHTS,
            is_display_resources_window: false,
            parked_thoughts: [],
            MEETING_STATUS_EDITING,
            MEETING_STATUS_STARTED,
            MEETING_STATUS_FINISHED,
            HAS_ACCESS_TO_START_AND_STOP_MEETING,
        }
    },
    inject: ['themes', 'faci'],
    components: {WindowComponent, KeyThoughtsChatComponent},
    template: `
        <div style="text-align: center; padding: 5px 0;" v-if="HAS_ACCESS_TO_START_AND_STOP_MEETING">
            <input type="button" v-if="faci.meeting_status == MEETING_STATUS_EDITING" value="Начать встречу" class="btn btn-outline-success" @click="start_meeting">
            <input type="button" v-if="faci.meeting_status == MEETING_STATUS_STARTED" value="Завершить встречу" class="btn btn-outline-success" @click="start_meeting">
            <span v-if="faci.meeting_status == MEETING_STATUS_FINISHED">Встреча завершена</span>
        </div>

        <key-thoughts-chat-component v-if="themes.length > 0"></key-thoughts-chat-component>
        <span v-else>Чтобы фиксировать ключевые мысли, пожалуйста, добавьте в шаге 3 темы, планируемые к обсуждению </span>

        <div style="padding: 1rem;">
						<div class="mb-3 input-group" v-if="HAS_ACCESS_TO_ADD_PARKED_THOUGHTS & faci.meeting_status == MEETING_STATUS_STARTED">
								<input name="parked_thought" id="parked_thought-field" class="form-control" v-model="parked_thought" placeholder="Парковка" title="Полезные мысли, не относящиеся к теме встречи"  @keyup.enter="add_parked_thought" type="text">
								<button type="button" @click="add_parked_thought" class="btn btn-outline-primary"> >>> </button>
						</div>
						<transition name="fade">
								<div v-if="sent_parked_thought" style="color: green;">Мысль сохранена: [[ sent_parked_thought ]]</div>
						</transition>
						<div style="text-decoration: underline; cursor: pointer;" @click="get_parked_thoughts">припаркованные мысли</div>
				</div>
        <window-component title="Припаркованные мысли" v-if="is_display_resources_window" @close="is_display_resources_window = false;">
            <div v-for="thought in parked_thoughts">
                <p style="margin-bottom: 0.25rem;"><b>[[ thought.username ]]:</b> [[ thought.parked_thought ]]</p>
            </div>
            <div v-if="parked_thoughts.length == 0">Отвлечённые мысли пока никто не парковал.</div>
        </window-component>
    `,
    methods: {
        add_parked_thought(event) {
            let self = this;
            if (!self.parked_thought) return;
            $.ajax({
                url: URL_FACI_EDITOR_PARKED_THOUGHTS,
                headers: {
                    "X-CSRFToken": CSRF_TOKEN,
                },
                dataType: 'json',
                data: {'parked_thought': self.parked_thought},
                success: function(result) {
                    set_valid_field(event.target.form, result.updated);
                    self.sent_parked_thought = self.parked_thought;
                    self.parked_thought = '';
                    setTimeout(function(){self.sent_parked_thought = '';}, 2000);
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
        get_parked_thoughts(event) {
            let self = this;
            $.ajax({
                url: URL_FACI_EDITOR_GET_PARKED_THOUGHTS,
                headers: {
                    "X-CSRFToken": CSRF_TOKEN,
                },
                dataType: 'json',
                data: {},
                success: function(result) {
                    self.parked_thoughts = result.parked_thoughts;
                    self.is_display_resources_window = true;
                },
                statusCode: {
                    403: function(xhr) {
                        alert(xhr.responseJSON.detail);
                    },
                },
                method: "post"
            });
        },
        start_meeting(event) {
            self = this;
            $.ajax({
                url: URL_FACI_EDITOR_START_MEETING,
                headers: {
                    "X-CSRFToken": CSRF_TOKEN,
                },
                dataType: 'json',
                data: {},
                success: function(result) {
                    self.faci.meeting_status = result.meeting_status;
                    self.faci.step = result.step;
                },
                error: function(jqxhr, a, b) {
                    console.log('error');
                    console.log(jqxhr.responseText);
                },
                method: "post"
            });
        },
    },
}
