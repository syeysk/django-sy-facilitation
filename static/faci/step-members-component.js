StepMembersComponent = {
    template: `
        <table style="width: 100%;" id="table_members">
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
        <input v-if="HAS_ACCESS_TO_ADD_MEMBERS & mode == 'view'" type="button" value="Добавить" @click="add_member" class="form-control">`,
    data() {
        return {
            member_list: JSON.parse(document.getElementById('members_json').textContent),
            mode: 'view',
            HAS_ACCESS_TO_ADD_MEMBERS,
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
                let member_item = $('#table_members > tr:last-child')[0].previousElementSibling;
                member_item.querySelector('.button_ss').click();
            }, 40);
        },
    },
    components: {
        StepMemberItemComponent
    },
}
