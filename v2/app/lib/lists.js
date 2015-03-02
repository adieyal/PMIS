module.exports = {
    colours: [
        '#85CABB',
        '#E6B744',
        '#D0D0AE',
        '#BFDFF6',
        '#BCBCBC',
        '#B6DED3',
        '#e377c2',
        '#7f7f7f',
        '#bcbd22',
        '#17becf'
    ],

    clusters: [
        { slug: "education", title: 'Education', view: "performance", colour: "#E8B96B" },
        { slug: "health", title: 'Health', view: "performance", colour: "#83C4BF" },
        { slug: "social-development", title: 'Social Development', view: "performance", colour: "#9691B0" },
        { slug: "culture-sports-science-and-recreation", title: 'Culture, Sports, Science and Recreation', view: "performance", colour: "#8CC7E9" },
        { slug: "community-safety-security-and-liaison", title: 'Community Safety, Security and Liaison', view: "performance", colour: "#B8B38B" },
        { slug: "economic-development-environment-and-tourism", title: 'Economic Development, Environment and Tourism', view: "performance", colour: "#BC7692" }
    ],

    districts: {
        ehlanzeni: 'Ehlanzeni District',
        gertsibande: 'Gert Sibande District',
        nkangala: 'Nkangala District'
    },

    projectPhases: {
        'unknown': 'Unknown',
        'planning': 'Planning',
        'implementation': 'Implementation',
        'completed': 'Completed',
        'final-accounts': 'Final accounts',
        'closed': 'Closed'
    },

    planningPhases: {
        "completed": "Planning Completed",
        "consultant-appointment": "Consultant Appt",
        "design-costing": "Design Costing",
        "documentation": "Documentation",
        "tender": "For Tender"
    },

    implementationGroups: {
        "completed": "Completed",
        "practical-completion": "Practical completion",
        "final-completion": "Final completion",
        "due-3months": "Due in 3 months"
    },
    districtSummaryGroups: {
        'financial-year': "Due in financial year",
        'three-months': "Due in 3 months",
        'this-month': "Due this month",
        'practical-completion': "Practical completion",
        'final-completion': "Final completion"
    }
};
