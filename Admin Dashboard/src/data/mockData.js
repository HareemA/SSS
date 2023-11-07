import { tokens } from "../theme";


export const mockBarData = [
  {
    time: "9:00",
    Men: 18,
    MenColor: "hsl(229, 70%, 50%)",
    Women: 2,
    WomenColor: "hsl(296, 70%, 50%)",
    Unidentified: 5,
    UnidentifiedColor: "hsl(340, 70%, 50%)",
  },
  {
    time: "10:00",
    Men: 9,
    MenColor: "hsl(307, 70%, 50%)",
    Women: 6,
    WomenColor: "hsl(111, 70%, 50%)",
    Unidentified: 1,
    UnidentifiedColor: "hsl(275, 70%, 50%)",
  },
  {
    time: "11:00",
    Men: 5,
    MenColor: "hsl(72, 70%, 50%)",
    Women: 5,
    WomenColor: "hsl(96, 70%, 50%)",
    Unidentified: 3,
    UnidentifiedColor: "hsl(256, 70%, 50%)",
  },
  {
    time: "12:00",
    Men: 11,
    MenColor: "hsl(257, 70%, 50%)",
    Women: 4,
    WomenColor: "hsl(326, 70%, 50%)",
    Unidentified: 3,
    UnidentifiedColor: "hsl(9, 70%, 50%)",
  },
  {
    time: "13:00",
    Men: 12,
    MenColor: "hsl(190, 70%, 50%)",
    Women: 13,
    WomenColor: "hsl(325, 70%, 50%)",
    Unidentified: 5,
    UnidentifiedColor: "hsl(285, 70%, 50%)",
  },
  {
    time: "14:00",
    Men: 10,
    MenColor: "hsl(208, 70%, 50%)",
    Women: 8,
    WomenColor: "hsl(334, 70%, 50%)",
    Unidentified: 3,
    UnidentifiedColor: "hsl(76, 70%, 50%)",
  },
  {
    time: "15:00",
    Men: 7,
    MenColor: "hsl(87, 70%, 50%)",
    Women: 6,
    WomenColor: "hsl(141, 70%, 50%)",
    Unidentified: 1,
    UnidentifiedColor: "hsl(274, 70%, 50%)",
  },
  {
    time: "16:00",
    Men: 5,
    MenColor: "hsl(87, 70%, 50%)",
    Women: 3,
    WomenColor: "hsl(141, 70%, 50%)",
    Unidentified: 2,
    UnidentifiedColor: "hsl(274, 70%, 50%)",
  },
  {
    time: "17:00",
    Men: 6,
    MenColor: "hsl(87, 70%, 50%)",
    Women: 5,
    WomenColor: "hsl(141, 70%, 50%)",
    Unidentified: 3,
    UnidentifiedColor: "hsl(274, 70%, 50%)",
  },
  {
    time: "18:00",
    Men: 9,
    MenColor: "hsl(87, 70%, 50%)",
    Women: 12,
    WomenColor: "hsl(141, 70%, 50%)",
    Unidentified: 1,
    UnidentifiedColor: "hsl(274, 70%, 50%)",
  },
  {
    time: "19:00",
    Men: 11,
    MenColor: "hsl(87, 70%, 50%)",
    Women: 15,
    WomenColor: "hsl(141, 70%, 50%)",
    Unidentified: 5,
    UnidentifiedColor: "hsl(274, 70%, 50%)",
  },
  {
    time: "20:00",
    Men: 13,
    MenColor: "hsl(87, 70%, 50%)",
    Women: 2,
    WomenColor: "hsl(141, 70%, 50%)",
    Unidentified: 5,
    UnidentifiedColor: "hsl(274, 70%, 50%)",
  },
  {
    time: "21:00",
    Men: 8,
    MenColor: "hsl(87, 70%, 50%)",
    Women: 2,
    WomenColor: "hsl(141, 70%, 50%)",
    Unidentified: 2,
    UnidentifiedColor: "hsl(274, 70%, 50%)",
  },
];



// export const mockPieData = [
//   {
//     id: "hack",
//     label: "hack",
//     value: 239,
//     color: "hsl(104, 70%, 50%)",
//   },
//   {
//     id: "make",
//     label: "make",
//     value: 170,
//     color: "hsl(162, 70%, 50%)",
//   },
//   {
//     id: "go",
//     label: "go",
//     value: 322,
//     color: "hsl(291, 70%, 50%)",
//   },
//   {
//     id: "lisp",
//     label: "lisp",
//     value: 503,
//     color: "hsl(229, 70%, 50%)",
//   },
//   {
//     id: "scala",
//     label: "scala",
//     value: 584,
//     color: "hsl(344, 70%, 50%)",
//   },
// ];

export const mockPieData = [
  {
    id: "Man",
    label: "Man",
    value: 239, // Replace with the actual number for men
    color: "hsl(104, 70%, 50%)",
  },
  {
    id: "Woman",
    label: "Woman",
    value: 170, // Replace with the actual number for women
    color: "hsl(162, 70%, 50%)",
  },
  {
    id: "Unidentified",
    label: "Unidentified",
    value: 322, // Replace with the actual number for unidentified
    color: "hsl(291, 70%, 50%)",
  },
];


export const mockLineDataCount = [
  
  {
    id: "ENTERED",
    color: tokens("dark").redAccent[600],
    data: [
      {
        x: "8:00",
        y: 191,
      },
      {
        x: "9:00",
        y: 136,
      },
      {
        x: "10:00",
        y: 91,
      },
      {
        x: "11:00",
        y: 190,
      },
      {
        x: "12:00",
        y: 211,
      },
      {
        x: "13:00",
        y: 152,
      },
      {
        x: "14:00",
        y: 189,
      },
      {
        x: "15:00",
        y: 152,
      },
      {
        x: "16:00",
        y: 8,
      },
      {
        x: "17:00",
        y: 197,
      },
      {
        x: "18:00",
        y: 107,
      },
      {
        x: "19:00",
        y: 170,
      },
      {
        x: "20:00",
        y: 170,
      },
      {
        x: "21:00",
        y: 170,
      },
      {
        x: "22:00",
        y: 170,
      },
    ],
  },
  {
    id: "LEFT",
    color: tokens("dark").blueAccent[400],
    data: [
      
      {
        x: "8:00",
        y: 150,
      },
      {
        x: "9:00",
        y: 120,
      },
      {
        x: "10:00",
        y: 197,
      },
      {
        x: "11:00",
        y: 129,
      },
      {
        x: "12:00",
        y: 151,
      },
      {
        x: "13:00",
        y: 85,
      },
      {
        x: "14:00",
        y: 123,
      },
      {
        x: "15:00",
        y: 33,
      },
      {
        x: "16:00",
        y: 22,
      },
      {
        x: "17:00",
        y: 3,
      },
      {
        x: "18:00",
        y: 117,
      },
      {
        x: "19:00",
        y: 88,
      },
      {
        x: "20:00",
        y: 29,
      },
      {
        x: "21:00",
        y: 37,
      },
      {
        x: "22:00",
        y: 55,
      },
      
    ],
  },
  {
    id: "MIN",
    color: tokens("dark").greenAccent[600],
    data: [
      // Data points for the "MIN" graph
      {
        x: "8:00",
        y: 123,
      },
      {
        x: "9:00",
        y: 192,
      },
      {
        x: "10:00",
        y: 197,
      },
      {
        x: "11:00",
        y: 119,
      },
      {
        x: "12:00",
        y: 37,
      },
      {
        x: "13:00",
        y: 25,
      },
      {
        x: "14:00",
        y: 63,
      },
      {
        x: "15:00",
        y: 143,
      },
      {
        x: "16:00",
        y: 112,
      },
      {
        x: "17:00",
        y: 139,
      },
      {
        x: "18:00",
        y: 167,
      },
      {
        x: "19:00",
        y: 138,
      },
      {
        x: "20:00",
        y: 190,
      },
      {
        x: "21:00",
        y: 162,
      },
      {
        x: "22:00",
        y: 71,
      },
    ],
  },
  {
    id: "MAX",
    color: tokens("dark").redAccent[300],
    data: [
      // Data points for the "MAX" graph
      {
        x: "8:00",
        y: 90,
      },
      {
        x: "9:00",
        y: 35,
      },
      {
        x: "10:00",
        y: 102,
      },
      {
        x: "11:00",
        y: 99,
      },
      {
        x: "12:00",
        y: 191,
      },
      {
        x: "13:00",
        y: 185,
      },
      {
        x: "14:00",
        y: 193,
      },
      {
        x: "15:00",
        y: 133,
      },
      {
        x: "16:00",
        y: 112,
      },
      {
        x: "17:00",
        y: 63,
      },
      {
        x: "18:00",
        y: 97,
      },
      {
        x: "19:00",
        y: 78,
      },
      {
        x: "20:00",
        y: 39,
      },
      {
        x: "21:00",
        y: 22,
      },
      {
        x: "22:00",
        y: 19,
      },
    ],
  },
];



export const mockLineDataWeekly = [
  
  {
    id: "ENTERED",
    color: tokens("dark").redAccent[600],
    data: [
      {
        x: "Mon",
        y: 191,
      },
      {
        x: "Tue",
        y: 136,
      },
      {
        x: "Wed",
        y: 91,
      },
      {
        x: "Thur",
        y: 190,
      },
      {
        x: "Fri",
        y: 211,
      },
      {
        x: "Sat",
        y: 152,
      },
      {
        x: "Sun",
        y: 189,
      },
      
    ],
  },
  {
    id: "LEFT",
    color: tokens("dark").blueAccent[400],
    data: [
      
      {
        x: "Mon",
        y: 150,
      },
      {
        x: "Tue",
        y: 120,
      },
      {
        x: "Wed",
        y: 197,
      },
      {
        x: "Thur",
        y: 129,
      },
      {
        x: "Fri",
        y: 151,
      },
      {
        x: "Sat",
        y: 85,
      },
      {
        x: "Sun",
        y: 123,
      },
      
    ],
  },
  {
    id: "MIN",
    color: tokens("dark").greenAccent[600],
    data: [
      // Data points for the "MIN" graph
      {
        x: "Mon",
        y: 123,
      },
      {
        x: "Tue",
        y: 192,
      },
      {
        x: "Wed",
        y: 197,
      },
      {
        x: "Thur",
        y: 119,
      },
      {
        x: "Fri",
        y: 37,
      },
      {
        x: "Sat",
        y: 25,
      },
      {
        x: "Sun",
        y: 63,
      },
      
    ],
  },
  {
    id: "MAX",
    color: tokens("dark").redAccent[300],
    data: [
      // Data points for the "MAX" graph
      {
        x: "Mon",
        y: 90,
      },
      {
        x: "Tue",
        y: 35,
      },
      {
        x: "Wed",
        y: 102,
      },
      {
        x: "Thur",
        y: 99,
      },
      {
        x: "Fri",
        y: 191,
      },
      {
        x: "Sat",
        y: 185,
      },
      {
        x: "Sun",
        y: 193,
      },
      
    ],
  },
];


export const mockLineDataMonthly = [
  {
    id: "Entered",
    color: tokens("dark").blueAccent[300],
    data: [
      
    { x: "1", y: 180 },
    { x: "2", y: 210 },
    { x: "3", y: 160 },
    { x: "4", y: 270 },
    { x: "5", y: 230 },
    { x: "6", y: 240 },
    { x: "7", y: 150 },
    { x: "8", y: 190 },
    { x: "9", y: 130 },
    { x: "10", y: 220 },
    { x: "11", y: 200 },
    { x: "12", y: 280 },
    { x: "13", y: 170 },
    { x: "14", y: 260 },
    { x: "15", y: 140 },
    { x: "16", y: 180 },
    { x: "17", y: 250 },
    { x: "18", y: 270 },
    { x: "19", y: 160 },
    { x: "20", y: 210 },
    { x: "21", y: 240 },
    { x: "22", y: 150 },
    { x: "23", y: 190 },
    { x: "24", y: 130 },
    { x: "25", y: 220 },
    { x: "26", y: 200 },
    { x: "27", y: 280 },
    { x: "28", y: 170 },
    { x: "29", y: 260 },
    { x: "30", y: 140 },
    ],
  },
  {
    id: "Left",
    color: tokens("dark").redAccent[600],
    data: [
      { x: "1", y: 200 },
      { x: "2", y: 160 },
      { x: "3", y: 230 },
      { x: "4", y: 280 },
      { x: "5", y: 150 },
      { x: "6", y: 190 },
      { x: "7", y: 270 },
      { x: "8", y: 220 },
      { x: "9", y: 250 },
      { x: "10", y: 180 },
      { x: "11", y: 140 },
      { x: "12", y: 260 },
      { x: "13", y: 280 },
      { x: "14", y: 210 },
      { x: "15", y: 240 },
      { x: "16", y: 270 },
      { x: "17", y: 190 },
      { x: "18", y: 200 },
      { x: "19", y: 150 },
      { x: "20", y: 270 },
      { x: "21", y: 250 },
      { x: "22", y: 210 },
      { x: "23", y: 220 },
      { x: "24", y: 190 },
      { x: "25", y: 230 },
      { x: "26", y: 240 },
      { x: "27", y: 280 },
      { x: "28", y: 160 },
      { x: "29", y: 170 },
      { x: "30", y: 150 },
    ],
  },
  {
    id: "Min",
    color: tokens("dark").greenAccent[600],
    data: [
      { x: "1", y: 130 },
    { x: "2", y: 270 },
    { x: "3", y: 180 },
    { x: "4", y: 220 },
    { x: "5", y: 250 },
    { x: "6", y: 170 },
    { x: "7", y: 190 },
    { x: "8", y: 280 },
    { x: "9", y: 140 },
    { x: "10", y: 160 },
    { x: "11", y: 260 },
    { x: "12", y: 240 },
    { x: "13", y: 210 },
    { x: "14", y: 230 },
    { x: "15", y: 190 },
    { x: "16", y: 270 },
    { x: "17", y: 220 },
    { x: "18", y: 250 },
    { x: "19", y: 180 },
    { x: "20", y: 140 },
    { x: "21", y: 200 },
    { x: "22", y: 260 },
    { x: "23", y: 130 },
    { x: "24", y: 190 },
    { x: "25", y: 220 },
    { x: "26", y: 250 },
    { x: "27", y: 160 },
    { x: "28", y: 280 },
    { x: "29", y: 270 },
    { x: "30", y: 230 },
    ],
  },
  {
    id: "Max",
    color: tokens("dark").redAccent[300],
    data: [
      { x: "1", y: 250 },
    { x: "2", y: 130 },
    { x: "3", y: 220 },
    { x: "4", y: 180 },
    { x: "5", y: 280 },
    { x: "6", y: 170 },
    { x: "7", y: 190 },
    { x: "8", y: 240 },
    { x: "9", y: 260 },
    { x: "10", y: 210 },
    { x: "11", y: 230 },
    { x: "12", y: 160 },
    { x: "13", y: 140 },
    { x: "14", y: 150 },
    { x: "15", y: 270 },
    { x: "16", y: 200 },
    { x: "17", y: 220 },
    { x: "18", y: 280 },
    { x: "19", y: 180 },
    { x: "20", y: 240 },
    { x: "21", y: 260 },
    { x: "22", y: 170 },
    { x: "23", y: 190 },
    { x: "24", y: 210 },
    { x: "25", y: 130 },
    { x: "26", y: 150 },
    { x: "27", y: 200 },
    { x: "28", y: 160 },
    { x: "29", y: 230 },
    { x: "30", y: 270 },
    ],
  },
];



export const mockLineDataGCount = [
  
  {
    id: "Group Count",
    color: tokens("dark").blueAccent[300],
    data: [
      {
        x: "8:00",
        y: 5,
      },
      {
        x: "9:00",
        y: 1,
      },
      {
        x: "10:00",
        y: 7,
      },
      {
        x: "11:00",
        y: 9,
      },
      {
        x: "12:00",
        y: 11,
      },
      {
        x: "13:00",
        y: 5,
      },
      {
        x: "14:00",
        y: 3,
      },
      {
        x: "15:00",
        y: 3,
      },
      {
        x: "16:00",
        y: 2,
      },
      {
        x: "17:00",
        y: 3,
      },
      {
        x: "18:00",
        y: 7,
      },
      {
        x: "19:00",
        y: 8,
      },
      {
        x: "20:00",
        y: 9,
      },
      {
        x: "21:00",
        y: 12,
      },
      {
        x: "22:00",
        y: 1,
      },
    ],
  },
  
];

export const mockDataGroup = 
[
    {
      "id": "group",
      "label": "Group",
      "value": 45,
      "color": "hsl(41, 70%, 50%)"
    },
    {
      "id": "individual",
      "label": "Individual",
      "value": 55,
      "color": "hsl(339, 70%, 50%)"
    },
    
];

export const mockUserData = 
[
  { id: 1,name: "Customer 1",visits: "10",gender: "M",age: "10",group: "N",timeIn: "10:15",timeOut: "12:35"},
    { id: 2, name: "Customer 2", visits: 15, gender: "F", age: 25, group: "A", timeIn: "11:30", timeOut: "14:45" },
    { id: 3, name: "Customer 3", visits: 8, gender: "M", age: 30, group: "N", timeIn: "09:45", timeOut: "12:20" },
    { id: 4, name: "Customer 4", visits: 12, gender: "F", age: 22, group: "A", timeIn: "10:00", timeOut: "13:15" },
    { id: 5, name: "Customer 5", visits: 18, gender: "M", age: 35, group: "N", timeIn: "08:15", timeOut: "11:30" },
    { id: 6, name: "Customer 6", visits: 14, gender: "F", age: 28, group: "A", timeIn: "11:45", timeOut: "15:00" },
    { id: 7, name: "Customer 7", visits: 9, gender: "M", age: 40, group: "N", timeIn: "09:00", timeOut: "12:15" },
    { id: 8, name: "Customer 8", visits: 11, gender: "F", age: 32, group: "A", timeIn: "10:30", timeOut: "13:45" },
    { id: 9, name: "Customer 9", visits: 16, gender: "M", age: 45, group: "N", timeIn: "08:45", timeOut: "12:00" },
    { id: 10, name: "Customer 10", visits: 20, gender: "F", age: 26, group: "A", timeIn: "12:00", timeOut: "15:15" }
];

