import { tokens } from "../theme";


export const mockBarData = [
  {
    dayOfWeek: "Monday",
    Men: 137,
    MenColor: "hsl(229, 70%, 50%)",
    Women: 96,
    WomenColor: "hsl(296, 70%, 50%)",
    Unidentified: 140,
    UnidentifiedColor: "hsl(340, 70%, 50%)",
  },
  {
    dayOfWeek: "Tuesday",
    Men: 55,
    MenColor: "hsl(307, 70%, 50%)",
    Women: 28,
    WomenColor: "hsl(111, 70%, 50%)",
    Unidentified: 29,
    UnidentifiedColor: "hsl(275, 70%, 50%)",
  },
  {
    dayOfWeek: "Wednesday",
    Men: 109,
    MenColor: "hsl(72, 70%, 50%)",
    Women: 23,
    WomenColor: "hsl(96, 70%, 50%)",
    Unidentified: 152,
    UnidentifiedColor: "hsl(256, 70%, 50%)",
  },
  {
    dayOfWeek: "Thursday",
    Men: 133,
    MenColor: "hsl(257, 70%, 50%)",
    Women: 52,
    WomenColor: "hsl(326, 70%, 50%)",
    Unidentified: 83,
    UnidentifiedColor: "hsl(9, 70%, 50%)",
  },
  {
    dayOfWeek: "Friday",
    Men: 81,
    MenColor: "hsl(190, 70%, 50%)",
    Women: 80,
    WomenColor: "hsl(325, 70%, 50%)",
    Unidentified: 35,
    UnidentifiedColor: "hsl(285, 70%, 50%)",
  },
  {
    dayOfWeek: "Saturday",
    Men: 66,
    MenColor: "hsl(208, 70%, 50%)",
    Women: 111,
    WomenColor: "hsl(334, 70%, 50%)",
    Unidentified: 18,
    UnidentifiedColor: "hsl(76, 70%, 50%)",
  },
  {
    dayOfWeek: "Sunday",
    Men: 80,
    MenColor: "hsl(87, 70%, 50%)",
    Women: 47,
    WomenColor: "hsl(141, 70%, 50%)",
    Unidentified: 49,
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
    id: "COUNT",
    color: tokens("dark").redAccent[200],
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

