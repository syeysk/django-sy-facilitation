StepPreparingComponent = {
    data() {
        return {
            faci: JSON.parse(document.getElementById('faci_json').textContent),
            MEETING_STATUS_STARTED,
            HAS_ACCESS_TO_EDIT_PREPARING,
        }
    },
    template: `
        <div v-if="HAS_ACCESS_TO_EDIT_PREPARING">
						<div class="mb-3 form-group" id="dt_meeting-group">
								<div class="form-floating">
										<input name="dt_meeting" class="form-control" id="dt_meeting-field" v-model="faci.dt_meeting" type="datetime-local">
										<label for="dt_meeting-field" class="form-label">Дата и время</label>
								</div>
						</div>
						<div class="mb-3 form-group" id="duration-group">
								<div class="form-floating">
										<input name="duration" class="form-control" id="duration-field" v-model="faci.duration" type="number" min="1">
										<label for="duration-field" class="form-label">Длительность</label>
								</div>
						</div>
						<div class="mb-3 form-group" id="place-group">
								<div class="form-floating">
										<input name="place" class="form-control" id="place-field" v-model="faci.place" type="text">
										<label for="place-field" class="form-label">Место</label>
								</div>
								<a v-if="is_url(faci.place)" :href="faci.place" rel="ugc" target="_blank">Открыть ссылку</a>
						</div>
						<input type="button" value="Сохранить" class="btn btn-secondary" @click="save">
  					<input type="button" :value="faci.meeting_status == MEETING_STATUS_STARTED ? 'Завершить встречу' : 'Начать встречу'" class="btn btn-secondary" id="button_start_meeting">
  			</div>
  			<div v-else>
						Дата и время: [[faci.dt_meeting]]
						<br>
						Длительность: [[faci.duration]] мин
						<br>
						Место: <a v-if="is_url(faci.place)" :href="faci.place" rel="ugc" target="_blank">открыть</a><span v-else>[[faci.place]]</span>
						<br>
  			</div>
    `,
    methods: {
        save(event) {
            let form = event.target.form;
            $.ajax({
                url: URL_FACI_EDITOR_PREPARING,
                headers: {
                    "X-CSRFToken": CSRF_TOKEN,
                },
                dataType: 'json',
                data: $(form).serialize(),
                success: function(result) {
                    set_valid_field(form, result.updated);
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
        }
    },
}
