KeyThoughtsChatComponent = {
    props: ['themes'],
    data() {
        let current_theme_index = 0;
        return {
            current_theme_index,
            current_theme_id: this.themes.length > 0 ? this.themes[current_theme_index].id.toString() : null,
            key_thought: '',
            key_thoughts: [],
            HAS_ACCESS_TO_ACTIVATE_THEME,
            HAS_ACCESS_TO_ADD_KEY_THOUGHTS,
            is_window_other_opened: false,
            window_theme_index: null,
        }
    },
    components: {WindowComponent},
    template: `
        <div v-for="theme, theme_index in themes" :key="theme.id" :data-theme-index="theme_index" class="theme-item">
            <div :style="'border-bottom: 1px solid white; color: white; /*border-radius: 3px;*/ padding: 12px 7px 12px 7px; /*margin-bottom: 1rem;*/ display: flex; justify-content: space-between; background-color: ' + (current_theme_index == theme_index.toString() ? '#51bd51;' : '#b9b9b9;')">
                <span :style="'cursor: default; font-weight: ' + (current_theme_index == theme_index.toString() ? '600;' : 'inherit;')">[[ theme.theme ]]</span>
                <span style="white-space: nowrap;">
                    <span v-if="current_theme_index == theme_index.toString()" style="cursor: pointer; border-radius: 3px; border: solid 1px white; padding: 3px; margin-right: 7px;"> || </span>
                    <span v-if="HAS_ACCESS_TO_ACTIVATE_THEME & current_theme_index == theme_index.toString()" @click="next_theme" style="cursor: pointer; border-radius: 3px; border: solid 1px white; padding: 3px; margin-right: 7px;" title="Перейти к следующий теме"> >> </span>
                    <span @click="open_other" style="cursor: pointer; border-radius: 3px; border: solid 1px white; padding: 3px 6px;" title="Дополнительные действия"> : </span>
                </span>
            </div>
            <div v-if="current_theme_index == theme_index.toString()" style="padding-left: 15px; padding-right: 15px; font-size: 10pt;">
                <div v-for="thought in key_thoughts">
                    <p style="margin-top: 0.5rem; margin-bottom: 0rem;"><b>[[ thought.username ]]:</b> [[ thought.key_thought ]]</p>
                </div>
								<div class="mb-3 input-group" v-if="HAS_ACCESS_TO_ADD_KEY_THOUGHTS"  style="margin-top: 1rem;">
										<textarea name="key_thoughts" id="key_thoughts-field" class="form-control" style="height: 80px; font-size: 10pt;"  v-model="key_thought" placeholder="Ключевая мысль"></textarea>
										<button type="button" @click="add_key_thoughts" class="btn btn-secondary"> >>> </button>
								</div>
            </div>
        </div>
				<window-component title="Дополнительные действия" v-if="is_window_other_opened" @close="is_window_other_opened = false;">
				    Для темы: <b>[[ themes[window_theme_index].theme ]]</b>
				    <br><br>
						<input type="button" value="Сохранить как PDF">
						<br><br>
						<input type="button" value="Перенести тему на другой холст">
				</window-component>
    `,
    mounted() {
        this.get_key_thoughts(false);
    },
    methods: {
        next_theme(event) {
            this.key_thoughts = [];
            this.current_theme_index += 1;
            if (this.current_theme_index >= this.themes.length) {
                this.current_theme_index = 0;
            }
            this.current_theme_id = this.themes[this.current_theme_index].id.toString();
            this.get_key_thoughts(true);
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
        get_key_thoughts(set_current) {
            let self = this;
            $.ajax({
                url: URL_FACI_EDITOR_GET_KEY_THOUGHTS,
                headers: {
                    "X-CSRFToken": CSRF_TOKEN,
                },
                dataType: 'json',
                data: set_current ? {theme: self.current_theme_id} : {},
                success: function(result) {
                    self.key_thoughts = result.key_thoughts;
                    if (!set_current) {
                        let theme_index = 0;
                        for (theme of self.themes) {
                            if (theme.id.toString() == result.current_theme_id.toString()) {
                                self.current_theme_index = theme_index;
                                self.current_theme_id = result.current_theme_id.toString();
                                break;
                            }
                            theme_index += 1;
                        }
                    }
                },
                statusCode: {
                    403: function(xhr) {
                        alert(xhr.responseJSON.detail);
                    },
                },
                method: "post"
            });
        },
        open_other(event) {
            this.window_theme_index = parseInt(event.target.closest('.theme-item').dataset.themeIndex);
            this.is_window_other_opened = true;
        }
    },
}
