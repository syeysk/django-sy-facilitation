StepPreparingComponent = {
    data() {
        return {
            HAS_ACCESS_TO_EDIT_PREPARING,
            MEETING_STATUS_EDITING,
        }
    },
    template: `
        <div v-if="HAS_ACCESS_TO_EDIT_PREPARING && faci.meeting_status == MEETING_STATUS_EDITING">
						<div class="mb-3 form-group" id="dt_meeting-group">
								<div class="form-floating">
										<input name="dt_meeting" class="form-control" id="dt_meeting-field" v-model="faci.dt_meeting" type="datetime-local">
										<label for="dt_meeting-field" class="form-label">Дата и время</label>
								</div>
						</div>
						<div class="mb-3 form-group" id="duration-group">
								<div class="form-floating">
										<input name="duration" class="form-control" id="duration-field" v-model="duration_of_all_themes" disabled type="number" :min="duration_of_all_themes" title="Суммарная длительность всех тем">
										<label for="duration-field" class="form-label">Длительность встречи, в минутах</label>
								</div>
						</div>
						<div class="mb-3 form-group" id="place-group">
								<div class="form-floating">
										<input name="place" class="form-control" id="place-field" v-model="faci.place" type="text">
										<label for="place-field" class="form-label">Место</label>
								</div>
								<a v-if="is_url(faci.place)" :href="faci.place" rel="ugc" target="_blank">[[ cutted_place ]]</a>
						</div>
						<div class="mb-3 form-group" id="form_of_feedback-group">
								<div class="form-floating" title="В конце встречи пользователи увидят приглашение пройти опрос">
										<input name="form_of_feedback" class="form-control" id="form_of_feedback-field" v-model="faci.form_of_feedback" type="text">
										<label for="form_of_feedback-field" class="form-label">Ссылка на форму обратной связи</label>
								</div>
						</div>
						<input type="button" value="Сохранить" class="btn btn-outline-primary" @click="save">
  			</div>
  			<div v-else>
						Дата и время: [[faci.dt_meeting]]
						<br>
						Длительность: [[faci.duration]] мин
						<br>
						Место: <a v-if="is_url(faci.place)" :href="faci.place" rel="ugc" target="_blank">[[ cutted_place ]]</a><span v-else>[[faci.place]]</span>
						<br>
  			</div>
    `,
    computed: {
        cutted_place() {
            let place = this.faci.place;
            let length_to_show = 50;
            if (place.length > length_to_show) {
                return place.slice(0, length_to_show / 2) +'...'+ place.slice(-(length_to_show / 2 - 3));
            }
            return place;
        },
    },
    inject: ['faci', 'themes', 'duration_of_all_themes'],
    methods: {
        save(event) {
            let self = this;
            let form = event.target.form;
            $.ajax({
                url: URL_FACI_EDITOR_PREPARING,
                headers: {"X-CSRFToken": CSRF_TOKEN},
                dataType: 'json',
                data: $(form).serialize(),
                success: function(result) {
                    set_valid_field(form, result.updated);
                    self.faci.step = result.step;
                },
                error: function(jqxhr, a, b) {
                    console.log(jqxhr.responseText);
                },
                statusCode: {
                    403: function(xhr) {
                        alert(xhr.responseJSON);
                    },
                    400: function(xhr) {
                        set_invalid_field(form, xhr.responseJSON);
                    },
                },
                method: "post"
            });
        },
        is_url(text) {
            return text.startsWith('https://') | text.startsWith('http://');
        },
    },
}
