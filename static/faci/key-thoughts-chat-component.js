KeyThoughtsChatComponent = {
    data() {
        let themes = JSON.parse(document.getElementById('themes_json').textContent);
        let current_theme_index = 0;
        return {
            faci: JSON.parse(document.getElementById('faci_json').textContent),
            themes,
            current_theme_index,
            current_theme_id: themes[current_theme_index].id.toString(),
        }
    },
    template: `
        <div v-for="theme in themes">
            <div :key="theme.id" :style="'border-radius: 3px; padding: 2px 2px 2px 5px; margin-bottom: 10px; display: flex; justify-content: space-between; background-color: ' + (current_theme_id == theme.id.toString() ? '#24a524;' : 'grey;')">
                <span :style="'color: white; font-weight: ' + (current_theme_id == theme.id.toString() ? '600;' : 'inherit;')">[[ theme.theme ]]</span>
                <span v-if="current_theme_id == theme.id.toString()" style="white-space: nowrap;">
                    <span  style="cursor: pointer; border-radius: 3px; border: solid 1px grey; padding: 3px;"> || </span>
                    <span @click="next_theme" style="cursor: pointer; border-radius: 3px; border: solid 1px grey; padding: 3px;"> >> </span>
                </span>
            </div>
						<div v-if="current_theme_id == theme.id.toString()" class="mb-3 input-group">
								<textarea name="key_thoughts" id="key_thoughts-field" class="form-control" style="height: 100px;"  v-model="faci.key_thoughts" placeholder="Ключевые мысли">[[ faci.key_thoughts ]]</textarea>
								<button type="button" @click="save_key_thoughts" class="btn btn-secondary"> >>> </button>
						</div>
        </div>
    `,
    methods: {
        next_theme(event) {
            this.current_theme_index += 1;
            if (this.current_theme_index >= this.themes.length) {
                this.current_theme_index = 0;
            }
            this.current_theme_id = this.themes[this.current_theme_index].id.toString();
        },
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
    },
}
