const MemberSearchItemComponent = {
    props: ['data'],
    template: `
        <div>
            <div>[[data.first_name]] [[data.last_name]]</div>
            <div>[[data.username]]</div>
        </div>
    `,
}
