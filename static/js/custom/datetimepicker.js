$('#startDateTime').datetimepicker({
    format: 'yyyy-mm-dd hh:ii:ss',
    todayBtn:true,
    todayHighlight:true,//today按钮高亮显示
    language: 'zh-CN',
    autoclose: true,
    forceParse: !1,
    fontAwesome:true
});
$('#endDateTime').datetimepicker({
    format: 'yyyy-mm-dd hh:ii:ss',
    todayBtn:true,
    todayHighlight:true,//today按钮高亮显示
    language: 'zh-CN',
    autoclose: true,
    forceParse: !1,
    fontAwesome:true
});
// format

// 这个是必须要设置的。

// String. 默认值: 'mm/dd/yyyy'

// 日期格式， p, P, h, hh, i, ii, s, ss, d, dd, m, mm, M, MM, yy, yyyy 的任意组合。
// weekStart

// Integer. 默认值：0

// 一周从哪一天开始。0（星期日）到6（星期六）
// startDate

// Date. 默认值：开始时间

// The earliest date that may be selected; all earlier dates will be disabled.
// endDate

// Date. 默认值：结束时间

// The latest date that may be selected; all later dates will be disabled.
// daysOfWeekDisabled  一周禁用的日期

// String, Array. 默认值: '', []

// Days of the week that should be disabled. Values are 0 (Sunday) to 6 (Saturday). Multiple values should be comma-separated. Example: disable weekends: '0,6' or [0,6].
// autoclose

// Boolean. 默认值：false

// 当选择一个日期之后是否立即关闭此日期时间选择器。
// startView

// Number, String. 默认值：2, 'month'

// 日期时间选择器打开之后首先显示的视图。 可接受的值：

//     0 or 'hour' for the hour view
//     1 or 'day' for the day view
//     2 or 'month' for month view (the default)
//     3 or 'year' for the 12-month overview
//     4 or 'decade' for the 10-year overview. Useful for date-of-birth datetimepickers.

// minView

// Number, String. 默认值：0, 'hour'

// 日期时间选择器所能够提供的最精确的时间选择视图。
// maxView

// Number, String. 默认值：4, 'decade'

// 日期时间选择器最高能展示的选择范围视图。
// todayBtn

// Boolean, "linked". 默认值: false

// 如果此值为true 或 "linked"，则在日期时间选择器组件的底部显示一个 "Today" 按钮用以选择当前日期。如果是true的话，"Today" 按钮仅仅将视图转到当天的日期，如果是"linked"，当天日期将会被选中。
// todayHighlight

// Boolean. 默认值: false

// 如果为true, 高亮当前日期。
// keyboardNavigation

// Boolean. 默认值: true

// 是否允许通过方向键改变日期。
// language

// String. 默认值: 'en'

// The two-letter code of the language to use for month and day names. These will also be used as the input's value (and subsequently sent to the server in the case of form submissions). Currently ships with English ('en'), German ('de'), Brazilian ('br'), and Spanish ('es') translations, but others can be added (see I18N below). If an unknown language code is given, English will be used.
// forceParse

// Boolean. 默认值: true

// 当选择器关闭的时候，是否强制解析输入框中的值。也就是说，当用户在输入框中输入了不正确的日期，选择器将会尽量解析输入的值，并将解析后的正确值按照给定的格式format设置到输入框中。
// minuteStep

// Number. 默认值: 5

// 此数值被当做步进值用于构建小时视图。对于每个 minuteStep 都会生成一组预设时间（分钟）用于选择。
// pickerReferer : 不建议使用

// String. 默认值: 'default' (other value available : 'input')

// The referer element to place the picker for the component implementation. If you want to place the picker just under the input field, just specify input.
// pickerPosition

// String. 默认值: 'bottom-right' (还支持 : 'bottom-left')

// 此选项当前只在组件实现中提供支持。通过设置选项可以讲选择器放倒输入框下方。
// viewSelect

// Number or String. 默认值: same as minView (supported values are: 'decade', 'year', 'month', 'day', 'hour')

// With this option you can select the view from which the date will be selected. By default it's the last one, however you can choose the first one, so at each click the date will be updated.
// showMeridian

// Boolean. 默认值: false

// This option will enable meridian views for day and hour views.
// initialDate

// Date or String. 默认值: new Date()

// You can initialize the viewer with a date. By default it's now, so you can specify yesterday or today at midnight ...