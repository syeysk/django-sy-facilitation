StepMembersComponent = {
    template: `
        <table style="width: 100%;">
            <tr style="text-align: center;">
                <th>Участник</th>
                <th>В каком вопросе компетентен</th>
                <!--<th>Кто пригласил</th>-->
                <th></th>
            </tr>
            <step-member-item-component
                v-for="member in member_list"
                :member="member"
                :member-mode="mode"
            ></step-member-item-component>
        </table>
        <input type="button" value="Добавить" @click="add_member" class="form-control">`,
    data() {
        return {
            member_list: JSON.parse(document.getElementById('members_json').textContent),
            mode: 'view',
        }
    },
    methods: {
        add_member(event) {
            this.mode = 'add',
            this.member_list.push({
                'id': '',
                'invited': '',
                'inviting': CURRENT_USERNAME,
                'for_what': '',
                'edit': true
            });
            setTimeout(function() {
                let member_item = $('#app_members > table > tr:last-child')[0].previousElementSibling;
                member_item.querySelector('.button_ss').click();
            }, 40);
        },
    },
    components: {
        StepMemberItemComponent
    },
}
