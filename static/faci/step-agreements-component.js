StepAgreementsComponent = {
    data() {
        return {
            faci: JSON.parse(document.getElementById('faci_json').textContent),
        }
    },
    template: `
				<div class="mb-3">
						<label for="other_agreements-field" class="form-label">Прочие договорённости</label>
						<textarea name="other_agreements" @blur="save_agreements" id="other_agreements-field" class="form-control" rows="10">[[ faci.other_agreements ]]</textarea>
				</div>
    `,
    methods: {
        save_agreements(event) {
            $.ajax({
                url: URL_FACI_EDITOR_AGREEMENTS,
                headers: {
                    "X-CSRFToken": CSRF_TOKEN,
                },
                dataType: 'json',
                data: $(event.target.form).serialize(),
                success: function(result) {
                    set_valid_field(event.target.form, result.updated);
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
