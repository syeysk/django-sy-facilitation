FaciComponent = {
    data() {
        return {
            STEP,
            faci: JSON.parse(document.getElementById('faci_json').textContent),
            themes: JSON.parse(document.getElementById('themes_json').textContent),
        }
    },
    provide() {
        return {
            open_block: this.open_block,
            faci: this.faci,
            themes: this.themes,
            duration_of_all_themes: Vue.computed(() => this.duration_of_all_themes),
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
    methods: {
        open_block(block) {
            let step = null;
            if (block == "members") step = 2;
            else if (block == "agenda") step = 3;
            else if (block == "preparing") step = 4;
            else if (block == "key_thoughts") step = 5;
            else if (block == "agreements") step = 6;

            if (step > this.STEP) this.STEP = step;
        },
    },
    computed: {
        duration_of_all_themes() {
            let theme;
            let total_duration = 0;
            for (theme of this.themes) {
                total_duration += theme.duration;
            }
            return total_duration | 1;
        }
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
												<div v-if="STEP < 2" class="form_sheet">Для открытия выполните 1-й шаг</div>
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
												<div v-if="STEP < 3" class="form_sheet"><span>Для открытия заполните, пожалуйста, список участников (2-й шаг)</span></div>
										</form>
								</div>

								<br>

								<div class="card accordion-item">
										<div class="accordion-header card-header accordion-button" data-bs-toggle="collapse" data-bs-target="#preparing_form" aria-expanded="true" aria-controls="panelsStayOpen-collapseOne">
												4. Подготовка
										</div>
										<form id="preparing_form" class="card-body accordion-collapse collapse show" @submit.prevent>
												<step-preparing-component></step-preparing-component>
												<div v-if="STEP < 4" class="form_sheet"><span>Откроется после выполнения 3-го шага</span></div>
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
												<div v-if="STEP < 5" class="form_sheet">Станет доступно во время встречи (после шага 4)</div>
										</form>
								</div>
						</div>

						<div class="col-sm-6">
								<div class="card accordion-item">
										<div class="accordion-header card-header accordion-button" data-bs-toggle="collapse" data-bs-target="#agreements_form" aria-expanded="true" aria-controls="panelsStayOpen-collapseOne">
												6. Договорённости
										</div>
										<form id="agreements_form" class="card-body accordion-collapse collapse show" @submit.prevent>
												<step-agreements-component id="app_agreements"></step-agreements-component>
												<div v-if="STEP < 6" class="form_sheet">Станет доступно после шага 4</div>
										</form>
								</div>
						</div>
				</div>
    `,
}
