StepKeyThoughtsComponent = {
    data() {
        return {
            faci: JSON.parse(document.getElementById('faci_json').textContent),
            sent_parked_thoughts: '',
            parked_thoughts: '',
        }
    },
    template: `
        <div class="mb-3 form-group">
            <div class="form-floating">
                <textarea name="key_thoughts" id="key_thoughts-field" class="form-control" style="height: 100px;"  v-model="faci.key_thoughts">[[ faci.key_thoughts ]]</textarea>
                <label for="key_thoughts-field" class="form-label">Ключевые мысли</label>
            </div>
        </div>
        <input type="button" value="Сохранить" @click="save_key_thoughts" class="btn btn-secondary">
        <br>
        <br>
        <div class="mb-3 input-group">
            <textarea name="parked_thoughts" id="parked_thoughts-field" class="form-control" v-model="parked_thoughts" placeholder="Парковка" title="Полезные мысли, не относящиеся к теме встречи">[[ faci.parked_thoughts ]]</textarea>
            <button type="button" @click="save_parked_thoughts" class="btn btn-secondary"> >>> </button>
        </div>
        <transition name="fade">
            <div v-if="sent_parked_thoughts" style="color: green;">Мысль сохранена: [[ sent_parked_thoughts ]]</div>
        </transition>
        <div style="text-decoration: underline; cursor: pointer;">посмотреть парковку</div>
    `,
    methods: {
        save_key_thoughts(event) {
            $.ajax({
                url: URL_FACI_EDITOR_KEY_THOUGHTS,
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
                method: "post"
            });
        },
        save_parked_thoughts(event) {
            let self = this;
            if (!self.parked_thoughts) return;
            $.ajax({
                url: URL_FACI_EDITOR_PARKED_THOUGHTS,
                headers: {
                    "X-CSRFToken": CSRF_TOKEN,
                },
                dataType: 'json',
                data: {'parked_thoughts': self.parked_thoughts},
                success: function(result) {
                    set_valid_field(event.target.form, result.updated);
                    self.sent_parked_thoughts = self.parked_thoughts;
                    self.parked_thoughts = '';
                    setTimeout(function(){self.sent_parked_thoughts = '';}, 2000);
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
}
