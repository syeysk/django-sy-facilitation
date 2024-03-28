FaciComponent = {
    data() {
        faci = JSON.parse(document.getElementById('faci_json').textContent);
        faci.when_started = faci.when_started ? luxon.DateTime.fromISO(faci.when_started) : null;
        faci.when_finished = faci.when_finished ? luxon.DateTime.fromISO(faci.when_finished) : null;
				faci.duration = faci.duration ? luxon.Duration.fromObject({minutes: faci.duration}) : null;
				faci.duration_actual = faci.duration_actual ? luxon.Duration.fromObject({minutes: faci.duration_actual}) : null;
        return {
            faci,
            themes: JSON.parse(document.getElementById('themes_json').textContent),
        }
    },
    provide() {
        return {
            faci: this.faci,
            themes: this.themes,
            duration_of_all_themes: Vue.computed(() => this.duration_of_all_themes),
            when_finished_plan: Vue.computed(() => this.when_finished_plan),
            duration_diff: Vue.computed(() => this.duration_diff),
            duration_actual_minutes: Vue.computed(() => this.duration_actual_minutes),
            duration_actual_hours: Vue.computed(() => this.duration_actual_hours),
        };
    },
    components: {
        StepAimComponent,
        StepMembersComponent,
        StepAgendaComponent,
        StepPreparingComponent,
        StepKeyThoughtsComponent,
        StepAgreementsComponent,
    },
    computed: {
        duration_of_all_themes() {  // return minutes as Integer
            let theme;
            let total_duration = 0;
            for (theme of this.themes) {
                total_duration += theme.duration;
            }
            return total_duration || 1;
        },
        duration_diff() {
            let faci = this.faci;
            if (faci.duration_actual && faci.duration) {
								return {
										minutes: Math.abs(Math.floor(faci.duration.as('minutes') - faci.duration_actual.as('minutes'))),
										hours: Math.abs(Math.floor(faci.duration.as('hours') - faci.duration_actual.as('hours'))),
										is_exact: faci.duration_actual.as('minutes') == faci.duration.as('minutes'),
										is_long: faci.duration_actual.as('minutes') > faci.duration.as('minutes'),
								}
						}
						return null;
        },
        duration_actual_minutes() {
            return this.faci.duration_actual ? this.faci.duration_actual.as('minutes') : null;
        },
        duration_actual_hours() {
            return this.faci.duration_actual ? Math.floor(this.faci.duration_actual.as('hours')) : null;
        },
    },
    template: `
		    <div class="row accordion">
						<div class="col-sm-6">
								<div class="card accordion-item">
										<div class="accordion-header accordion-button card-header" data-bs-toggle="collapse" data-bs-target="#aim_form" aria-expanded="true" aria-controls="panelsStayOpen-collapseOne">
												1. Цель
										</div>
										<form id="aim_form" class="card-body accordion-collapse collapse show" @submit.prevent>
												<step-aim-component></step-aim-component>
										</form>
								</div>

								<br>

								<div class="card accordion-item">
										<div class="accordion-header card-header accordion-button" data-bs-toggle="collapse" data-bs-target="#members_form" aria-expanded="true" aria-controls="panelsStayOpen-collapseOne">
												2. Участники
										</div>
										<form id="members_form" class="card-body accordion-collapse collapse show" @submit.prevent>
												<step-members-component></step-members-component>
												<div v-if="faci.step < 2" class="form_sheet">Для открытия выполните 1-й шаг</div>
										</form>
								</div>
						</div>

						<br>

						<div class="col-sm-6">
								<div class="card accordion-item">
										<div class="accordion-header card-header accordion-button" data-bs-toggle="collapse" data-bs-target="#agenda_form" aria-expanded="true" aria-controls="panelsStayOpen-collapseOne">
												3. Повестка
										</div>
										<form id="agenda_form" class="card-body accordion-collapse collapse show" @submit.prevent>
												<step-agenda-component></step-agenda-component>
												<div v-if="faci.step < 3" class="form_sheet"><span>Для открытия заполните, пожалуйста, список участников (2-й шаг)</span></div>
										</form>
								</div>

								<br>

								<div class="card accordion-item">
										<div class="accordion-header card-header accordion-button" data-bs-toggle="collapse" data-bs-target="#preparing_form" aria-expanded="true" aria-controls="panelsStayOpen-collapseOne">
												4. Подготовка
										</div>
										<form id="preparing_form" class="card-body accordion-collapse collapse show" @submit.prevent>
												<step-preparing-component></step-preparing-component>
												<div v-if="faci.step < 4" class="form_sheet"><span>Откроется после выполнения 3-го шага</span></div>
										</form>
								</div>
						</div>
				</div>

				<br>

				<div class="row accordion">
						<div class="col-sm-6">
								<div class="card accordion-item">
										<div class="accordion-header card-header accordion-button" data-bs-toggle="collapse" data-bs-target="#key_thoughts_form" aria-expanded="true" aria-controls="panelsStayOpen-collapseOne">
												5. Ключевые мысли
										</div>
										<form id="key_thoughts_form" class="card-body accordion-collapse collapse show" style="padding: 0 0 0 0;" @submit.prevent>
												<step-key-thoughts-component></step-key-thoughts-component>
												<div v-if="faci.step < 5" class="form_sheet">Станет доступно во время встречи (после шага 4)</div>
										</form>
								</div>
						</div>

						<div class="col-sm-6">
								<div class="card accordion-item">
										<div class="accordion-header card-header accordion-button" data-bs-toggle="collapse" data-bs-target="#agreements_form" aria-expanded="true" aria-controls="panelsStayOpen-collapseOne">
												6. Договорённости
										</div>
										<form id="agreements_form" class="card-body accordion-collapse collapse show" @submit.prevent>
												<step-agreements-component></step-agreements-component>
												<div v-if="faci.step < 6" class="form_sheet">Станет доступно, как только начнётcя встреча</div>
										</form>
								</div>
						</div>
				</div>
    `,
}
