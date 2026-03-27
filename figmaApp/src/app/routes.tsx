import { createBrowserRouter } from "react-router";
import {
  Home,
  RealtimeAnalysis,
  RealtimeReport,
  UploadAnalysis,
  UploadResult,
} from "./pages";

export const router = createBrowserRouter([
  {
    path: "/",
    Component: Home,
  },
  {
    path: "/realtime",
    Component: RealtimeAnalysis,
  },
  {
    path: "/realtime/report",
    Component: RealtimeReport,
  },
  {
    path: "/upload",
    Component: UploadAnalysis,
  },
  {
    path: "/upload/result",
    Component: UploadResult,
  },
]);
