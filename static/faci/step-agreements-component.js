StepAgreementsComponent = {
    data() {
        return {
            agreements: JSON.parse(document.getElementById('agreements_json').textContent),
            HAS_ACCESS_TO_ADD_AGREEMENT,
            agreement: '',
        }
    },
    template: `
        <div>
            <div v-for="agreement in agreements" :key="agreement.id">
                <div style="display: flex; justify-content: space-between;">
                    <span><input type="checkbox"> [[ agreement.agreement ]]</span>
                    <span>:</span>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 10pt; color: grey;">
										<span v-if="agreement.responsible_username">Ответственный: [[ agreement.responsible_username ]] мин</span>
										<span v-if="agreement.expire_dt">Срок: [[ agreement.expire_dt ]]</span>
							  </div>
            </div>
        </div>
        <div class="mb-3 input-group" v-if="HAS_ACCESS_TO_ADD_AGREEMENT">
						<input name="agreement" id="agreement-field" class="form-control" v-model="agreement" placeholder="Итоговое соглашение" title="Напишите, о чём в итоге договорились"  @keyup.enter="add_agreement" type="text">
						<button type="button" @click="add_agreement" class="btn btn-outline-primary"> >>> </button>
				</div>
    `,
    methods: {
        add_agreement(event) {
            self = this;
            $.ajax({
                url: URL_FACI_ADD_AGREEMENT,
                headers: {"X-CSRFToken": CSRF_TOKEN},
                dataType: 'json',
                data: {'agreement': self.agreement},
                success: function(result) {
                    set_valid_field(event.target.form, result.updated);
                    self.agreements.push(
                        {id: result.id, agreement: self.agreement, expire_dt: null, done_dt: null, responsible_username: ''},
                    );
                    self.agreement = '';
                },
                statusCode: {
                    403: function(xhr) {
                        alert(xhr.responseJSON.detail);
                    },
                    400: function(xhr) {
                        set_invalid_field(event.target.form, xhr.responseJSON);
                    },
                },
                method: "post",
            });
        }
    },
}
