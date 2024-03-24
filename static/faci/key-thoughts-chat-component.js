KeyThoughtsChatComponent = {
    props: ['themes'],
    data() {
        let current_theme_index = 0;
        return {
            current_theme_index,
            current_theme_id: this.themes.length > 0 ? this.themes[current_theme_index].id.toString() : null,
            key_thought: '',
            key_thoughts: [],
        }
    },
    template: `
        <div v-for="theme in themes">
            <div :key="theme.id" :style="'color: white; border-radius: 3px; padding: 12px 7px 12px 7px; margin-bottom: 1rem; display: flex; justify-content: space-between; background-color: ' + (current_theme_id == theme.id.toString() ? '#51bd51;' : '#b9b9b9;')">
                <span :style="'font-weight: ' + (current_theme_id == theme.id.toString() ? '600;' : 'inherit;')">[[ theme.theme ]]</span>
                <span v-if="current_theme_id == theme.id.toString()" style="white-space: nowrap;">
                    <span  style="cursor: pointer; border-radius: 3px; border: solid 1px white; padding: 3px; margin-right: 5px;"> || </span>
                    <span @click="next_theme" style="cursor: pointer; border-radius: 3px; border: solid 1px white; padding: 3px;" title="Перейти к следующий теме"> >> </span>
                </span>
            </div>
            <div v-if="current_theme_id == theme.id.toString()" style="padding-left: 15px; padding-right: 15px; font-size: 10pt;">
                <div v-for="thought in key_thoughts">
                    <p style="margin-bottom: 0.25rem;"><b>[[ thought.username ]]:</b> [[ thought.key_thought ]]</p>
                </div>
                <br>
								<div class="mb-3 input-group">
										<textarea name="key_thoughts" id="key_thoughts-field" class="form-control" style="height: 80px; font-size: 10pt;"  v-model="key_thought" placeholder="Ключевая мысль"></textarea>
										<button type="button" @click="add_key_thoughts" class="btn btn-secondary"> >>> </button>
								</div>
            </div>
        </div>
    `,
    mounted() {
        this.get_key_thoughts();
    },
    methods: {
        next_theme(event) {
            this.key_thoughts = [];
            this.current_theme_index += 1;
            if (this.current_theme_index >= this.themes.length) {
                this.current_theme_index = 0;
            }
            this.current_theme_id = this.themes[this.current_theme_index].id.toString();
            this.get_key_thoughts();
        },
        add_key_thoughts(event) {
            let self = this;
            if (!self.key_thought) return;
            $.ajax({
                url: URL_FACI_EDITOR_ADD_KEY_THOUGHT,
                headers: {
                    "X-CSRFToken": CSRF_TOKEN,
                },
                dataType: 'json',
                data: {key_thought: self.key_thought, theme: self.current_theme_id},
                success: function(result) {
                    set_valid_field(event.target.form, result.updated);
                    self.key_thoughts.push({username: CURRENT_USERNAME, key_thought: self.key_thought})
                    self.key_thought = '';
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
        get_key_thoughts() {
            let self = this;
            $.ajax({
                url: URL_FACI_EDITOR_GET_KEY_THOUGHTS,
                headers: {
                    "X-CSRFToken": CSRF_TOKEN,
                },
                dataType: 'json',
                data: {theme: self.current_theme_id},
                success: function(result) {
                    self.key_thoughts = result.key_thoughts;
                },
                statusCode: {
                    403: function(xhr) {
                        alert(xhr.responseJSON.detail);
                    },
                },
                method: "post"
            });
        },
    },
}
