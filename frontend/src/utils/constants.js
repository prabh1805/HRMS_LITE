export const API_BASE_URL =
  import.meta.env.VITE_API_URL || "http://localhost:8000/api";

export const ATTENDANCE_STATUS = {
  PRESENT: "PRESENT",
  ABSENT: "ABSENT",
};

export const STATUS_COLORS = {
  PRESENT: "bg-green-100 text-green-800",
  ABSENT: "bg-red-100 text-red-800",
};
