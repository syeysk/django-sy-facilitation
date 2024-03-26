StepAimComponent = {
    data() {
        return {
            aim_type_choices: JSON.parse(document.getElementById('aim_type_choices_json').textContent),
            faci: JSON.parse(document.getElementById('faci_json').textContent),
            HAS_ACCESS_TO_EDIT_AIM,
            STATIC_PREFIX,
            STEP,
        }
    },
    template: `
        <template v-if="HAS_ACCESS_TO_EDIT_AIM">
						<div class="mb-3 form-group" id="aim_type-group">
								<div class="form-floating">
										<select name="aim_type" class="form-select" id="aim_type-field">
												<option v-for="(aim_type_name, aim_type_id, index) in aim_type_choices" :value="aim_type_id" :selected="aim_type_id == faci.aim_type">[[ aim_type_name ]]</option>
										</select>
										<label for="aim_type-field" class="form-label">Вид встречи</label>
								</div>
						</div>
						<div class="mb-3 form-group" id="aim-group">
								<div class="form-floating">
										<input name="aim" class="form-control" id="aim-field" v-model="faci.aim">
										<label for="aim-field" class="form-label">Что мы пытаемся достичь?</label>
								</div>
						</div>
						<div class="mb-3 form-group" id="if_not_reached-group">
								<div class="form-floating">
										<input name="if_not_reached" class="form-control" id="if_not_reached-field" v-model="faci.if_not_reached">
										<label for="if_not_reached-field" class="form-label">Что произойдёт, если цель не будет достигнута?</label>
								</div>
						</div>
						<div class="mb-3 form-group" id="solutions-group">
								<div class="form-floating">
										 <input name="solutions" class="form-control" id="solutions-field" v-model="faci.solutions">
										 <label for="solutions-field" class="form-label">Первоначальные решения</label>
								</div>
						</div>

						<input type="button" :value="'Сохранить' + (STEP == 1 ? ' и перейти к заполнению участников' : '')" class="btn btn-secondary" @click="save_form_aim">
				</template>
				<template v-else>
						<template v-for="(aim_type_name, aim_type_id, index) of aim_type_choices">
								<div v-if="aim_type_id == faci.aim_type" style="text-align: center;">
										[[ aim_type_name ]] <br>
										<img style="width: 50px;" :src="STATIC_PREFIX + 'faci/aim_type/' + aim_type_id + '.svg'" :alt="aim_type_name" :title="aim_type_name"> <br>
										<template v-if="faci.aim">
												[[ faci.aim ]] <br>
										</template>
								</div>
						</template>

						<template v-if="faci.if_not_reached">
								<br> <span style="font-style: italic;"> Что произойдёт, если цель не будет достигнута:</span> <br> [[ faci.if_not_reached ]] <br>
						</template>

						<template v-if="faci.solutions">
								<br> <span style="font-style: italic;">Первоначальные решения:</span> <br>[[ faci.solutions ]] <br>
						</template>
				</template>
    `,
    inject: ['open_block'],
    methods: {
        save_form_aim(event) {
            $.ajax({
                url: URL_FACI_EDITOR_AIM,
                headers: {"X-CSRFToken": CSRF_TOKEN},
                dataType: 'json',
                data: $(event.target.form).serialize(),
                success: function(result) {
                    set_valid_field(event.target.form, result.updated);
                    try {
                        history.pushState(null, null, location.href.replace('/new', '/'+result['id']));
                        self.open_block(result['open_block']);
                    } catch(e) {}
                },
                error: function(jqxhr, a, b) {
                    console.log(jqxhr.responseText);
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
        }
    },
}
