var masterTemplate = [
    [
        {
            type: "frameSettings",
            token: "initial-frame",
            height: 550,
            chainedFrame: "partnership-frame"
        },
        {
            type: "input",
            dataType: "text",
            required: true,
            label: "Name*",
            id: "name",
            placeHolder: null,
            defaultValue: null,
            style: null
        },
        {
            type: "input",
            dataType: "text",
            required: true,
            label: "Phone*",
            id: "phone",
            placeHolder: null,
            defaultValue: null,
            style: null
        },
        {
            type: "input",
            dataType: "email",
            required: true,
            label: "E-mail*",
            id: "email",
            placeHolder: null,
            defaultValue: null,
            style: null
        },
        {
            type: "select",
            label: "Type*",
            id: "category",
            selected: 0,
            options: [
                {
                    value: "partnership",
                    title: "Partnership",
                    chainedFrame: "partnership-frame"
                },
                {
                    value: "learing",
                    title: "Enrollment",
                    chainedFrame: "learning-frame"
                },
                {
                    value: "support",
                    title: "Tech support",
                    chainedFrame: "support-frame"
                }
            ]
        },
    ],
    [
        {
            type: "frameSettings",
            token: "support-frame",
            height: 550,
            chainedFrame: "FINAL"
        },
        {
            type: "select",
            label: "Product*",
            id: "product",
            selected: 0,
            options: [
                {
                    value: "iphone",
                    title: "iPhone"
                },
                {
                    value: "mac",
                    title: "macBook"
                },
                {
                    value: "ipad",
                    title: "iPad"
                },
            ]
        },
        {
            type: "input",
            dataType: "text",
            required: true,
            label: "OS Vertion*",
            id: "version",
            placeHolder: null,
            defaultValue: null,
            style: null
        },
        {
            type: "textarea",
            required: true,
            label: "Message*",
            id: "problem",
            defaultValue: null,
            style: "height: 250px;"
        },
    ],
    [
        {
            type: "frameSettings",
            token: "partnership-frame",
            height: 550,
            chainedFrame: "FINAL"
        },
        {
            type: "input",
            dataType: "text",
            required: true,
            label: "Company*",
            id: "company",
            placeHolder: null,
            defaultValue: null,
            style: null
        },
        {
            type: "input",
            dataType: "text",
            label: "Web-site",
            id: "website",
            placeHolder: null,
            defaultValue: null,
            style: null
        },
        {
            type: "textarea",
            required: true,
            label: "Message*",
            id: "msg",
            defaultValue: null,
            style: "height: 250px;"
        },
    ],
    [
        {
            type: "frameSettings",
            token: "learning-frame",
            height: 650,
            chainedFrame: "FINAL"
        },
        {
            type: "input",
            dataType: "text",
            required: true,
            label: "Company*",
            id: "company",
            placeHolder: null,
            defaultValue: null,
            style: null
        },
        {
            type: "input",
            dataType: "text",
            required: true,
            label: "Participants*",
            id: "participants",
            placeHolder: "Number of participants",
            defaultValue: null,
            style: null
        },
        {
            type: "input",
            dataType: "text",
            required: true,
            label: "Course*",
            id: "program",
            placeHolder: "Choose learning course",
            defaultValue: null,
            style: null
        },
        {
            type: "input",
            dataType: "text",
            label: "Date",
            id: "date",
            placeHolder: null,
            defaultValue: null,
            style: null
        },
        {
            type: "textarea",
            required: true,
            label: "Message*",
            id: "msg2",
            defaultValue: null,
            style: "height: 250px;"
        },
    ]
];
