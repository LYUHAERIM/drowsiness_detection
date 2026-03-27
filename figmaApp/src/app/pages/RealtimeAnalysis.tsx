import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router";
import { ArrowLeft, FileText, Camera, Circle, AlertTriangle, CircleDot } from "lucide-react";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Badge } from "../components/ui/badge";

type Status = "NORMAL" | "DROWSY" | "ABSENCE";

interface Participant {
  id: number;
  name: string;
  status: Status;
  position: { x: number; y: number; width: number; height: number };
}

interface Alert {
  id: number;
  status: Status;
  timestamp: string;
  participant: string;
}

export function RealtimeAnalysis() {
  const navigate = useNavigate();
  const videoRef = useRef<HTMLVideoElement>(null);
  const [currentTime, setCurrentTime] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [alerts, setAlerts] = useState<Alert[]>([]);

  const [participants, setParticipants] = useState<Participant[]>([
    { id: 1, name: "강경미", status: "NORMAL", position: { x: 5, y: 5, width: 15, height: 25 } },
    { id: 2, name: "박해슬", status: "NORMAL", position: { x: 5, y: 35, width: 15, height: 25 } },
    { id: 3, name: "김주원 (나)", status: "NORMAL", position: { x: 5, y: 65, width: 15, height: 25 } },
    { id: 4, name: "조인선", status: "NORMAL", position: { x: 78, y: 5, width: 17, height: 25 } },
    { id: 5, name: "김태완", status: "NORMAL", position: { x: 78, y: 35, width: 17, height: 25 } },
  ]);

  const [webcamStream, setWebcamStream] = useState<MediaStream | null>(null);
  const webcamRef = useRef<HTMLVideoElement>(null);

  // Initialize webcam
  useEffect(() => {
    async function setupWebcam() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        setWebcamStream(stream);
        if (webcamRef.current) {
          webcamRef.current.srcObject = stream;
        }
      } catch (err) {
        console.error("Error accessing webcam:", err);
      }
    }
    setupWebcam();

    return () => {
      if (webcamStream) {
        webcamStream.getTracks().forEach(track => track.stop());
      }
    };
  }, []);

  // Simulate status changes
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTime(prev => prev + 1);

      // Randomly change status for demo
      if (Math.random() > 0.9) {
        const randomParticipant = Math.floor(Math.random() * participants.length);
        const statuses: Status[] = ["NORMAL", "DROWSY", "ABSENCE"];
        const newStatus = statuses[Math.floor(Math.random() * statuses.length)];

        setParticipants(prev =>
          prev.map((p, idx) =>
            idx === randomParticipant ? { ...p, status: newStatus } : p
          )
        );

        if (newStatus !== "NORMAL") {
          const newAlert: Alert = {
            id: Date.now(),
            status: newStatus,
            timestamp: new Date().toLocaleTimeString('ko-KR', { hour12: false }),
            participant: participants[randomParticipant].name,
          };
          setAlerts(prev => [newAlert, ...prev].slice(0, 8));
        }
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [participants]);

  const getStatusColor = (status: Status) => {
    switch (status) {
      case "NORMAL":
        return "border-emerald-500/50 bg-emerald-500/5";
      case "DROWSY":
        return "border-amber-500/50 bg-amber-500/5";
      case "ABSENCE":
        return "border-red-500/50 bg-red-500/5";
    }
  };

  const getStatusBadgeColor = (status: Status) => {
    switch (status) {
      case "NORMAL":
        return "bg-emerald-500/20 text-emerald-300 border-emerald-500/30";
      case "DROWSY":
        return "bg-amber-500/20 text-amber-300 border-amber-500/30";
      case "ABSENCE":
        return "bg-red-500/20 text-red-300 border-red-500/30";
    }
  };

  const getAlertConfig = (status: Status) => {
    switch (status) {
      case "NORMAL":
        return {
          icon: CircleDot,
          label: "정상",
          description: "수업에 집중하고 있습니다",
          bgColor: "bg-emerald-500/5 border-emerald-500/20",
          iconColor: "text-emerald-400",
          labelColor: "text-emerald-300",
        };
      case "DROWSY":
        return {
          icon: AlertTriangle,
          label: "졸음",
          description: "졸음이 감지되었습니다",
          bgColor: "bg-amber-500/5 border-amber-500/20",
          iconColor: "text-amber-400",
          labelColor: "text-amber-300",
        };
      case "ABSENCE":
        return {
          icon: Circle,
          label: "이탈",
          description: "자리를 이탈했습니다",
          bgColor: "bg-red-500/5 border-red-500/20",
          iconColor: "text-red-400",
          labelColor: "text-red-300",
        };
    }
  };

  return (
    <div className="min-h-screen bg-[#0a0e1a]">
      {/* Header */}
      <div className="border-b border-slate-800/50 bg-[#151b2e]/80 backdrop-blur-sm sticky top-0 z-10">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Button
                variant="ghost"
                size="icon"
                onClick={() => navigate("/")}
                className="text-slate-400 hover:text-slate-100 hover:bg-slate-800"
              >
                <ArrowLeft className="w-5 h-5" />
              </Button>
              <div>
                <div className="flex items-center gap-3">
                  <h1 className="text-xl text-slate-50">실시간 분석</h1>
                  <div className="flex items-center gap-2 px-2 py-1 rounded bg-blue-500/10 border border-blue-500/20">
                    <div className="w-2 h-2 rounded-full bg-blue-400 animate-pulse" />
                    <span className="text-xs text-blue-300">LIVE</span>
                  </div>
                </div>
                <p className="text-sm text-slate-500">Demo Mode - 2분 영상</p>
              </div>
            </div>
            <Button
              onClick={() => navigate("/realtime/report")}
              className="bg-blue-600 hover:bg-blue-700 border-0"
            >
              <FileText className="w-4 h-4 mr-2" />
              리포트 보기
            </Button>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-6">
        <div className="grid lg:grid-cols-[1fr_380px] gap-6">
          {/* Main Video Area */}
          <div className="space-y-4">
            <Card className="overflow-hidden bg-[#151b2e] border-slate-800/50">
              <CardContent className="p-0">
                <div className="relative aspect-video bg-slate-950/50">
                  {/* Background Demo Video */}
                  <img
                    src="figma:asset/80652276761e4f9c48177aee51bd30dc4ad0897a.png"
                    alt="Demo video"
                    className="w-full h-full object-cover"
                  />

                  {/* Participant Overlays with Bounding Boxes */}
                  {participants.map((participant) => (
                    <div
                      key={participant.id}
                      className={`absolute border-2 transition-all ${getStatusColor(participant.status)}`}
                      style={{
                        left: `${participant.position.x}%`,
                        top: `${participant.position.y}%`,
                        width: `${participant.position.width}%`,
                        height: `${participant.position.height}%`,
                      }}
                    >
                      {/* Name and Status Badge */}
                      <div className="absolute -bottom-7 left-0 flex items-center gap-2">
                        <span className="text-xs text-slate-100 bg-slate-900/90 px-2 py-1 rounded backdrop-blur-sm">
                          {participant.name}
                        </span>
                        <Badge className={`text-xs border ${getStatusBadgeColor(participant.status)}`}>
                          {participant.status}
                        </Badge>
                      </div>

                      {/* Webcam Overlay for "나" */}
                      {participant.name.includes("나") && (
                        <div className="absolute inset-0 overflow-hidden rounded">
                          <video
                            ref={webcamRef}
                            autoPlay
                            playsInline
                            muted
                            className="w-full h-full object-cover"
                          />
                          <div className="absolute top-2 right-2 bg-red-500/80 rounded-full p-1">
                            <Camera className="w-3 h-3 text-white" />
                          </div>
                        </div>
                      )}
                    </div>
                  ))}

                  {/* Video Controls Overlay */}
                  <div className="absolute bottom-4 left-4 right-4">
                    <div className="bg-slate-900/90 backdrop-blur-sm rounded-lg px-4 py-3 border border-slate-800/50">
                      <div className="flex items-center gap-4">
                        <Button
                          size="sm"
                          variant="ghost"
                          onClick={() => setIsPlaying(!isPlaying)}
                          className="text-slate-100 hover:bg-slate-800"
                        >
                          {isPlaying ? "일시정지" : "재생"}
                        </Button>
                        <div className="flex-1">
                          <div className="flex items-center gap-3">
                            <span className="text-xs text-slate-400 tabular-nums min-w-[45px]">
                              {Math.floor(currentTime / 60)}:{(currentTime % 60).toString().padStart(2, "0")}
                            </span>
                            <div className="flex-1 h-1.5 bg-slate-800 rounded-full overflow-hidden">
                              <div
                                className="h-full bg-blue-500 transition-all"
                                style={{ width: `${(currentTime / 120) * 100}%` }}
                              />
                            </div>
                            <span className="text-xs text-slate-400 tabular-nums">2:00</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Status Sidebar */}
          <div className="space-y-4">
            {/* Current Status */}
            <Card className="bg-[#151b2e] border-slate-800/50">
              <CardHeader>
                <CardTitle className="text-slate-100 text-base">현재 상태</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                {participants.map((participant) => (
                  <div
                    key={participant.id}
                    className="flex items-center justify-between p-3 bg-slate-900/30 rounded-lg border border-slate-800/30"
                  >
                    <span className="text-sm text-slate-300">{participant.name}</span>
                    <Badge
                      className={`text-xs border ${getStatusBadgeColor(participant.status)}`}
                    >
                      {participant.status}
                    </Badge>
                  </div>
                ))}
              </CardContent>
            </Card>

            {/* Alerts - Status-focused design */}
            <Card className="bg-[#151b2e] border-slate-800/50">
              <CardHeader>
                <CardTitle className="text-slate-100 text-base">실시간 알림</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                {alerts.length === 0 ? (
                  <div className="text-center py-8">
                    <p className="text-sm text-slate-600">알림이 없습니다</p>
                  </div>
                ) : (
                  <div className="space-y-2 max-h-[500px] overflow-y-auto">
                    {alerts.map((alert) => {
                      const config = getAlertConfig(alert.status);
                      const Icon = config.icon;

                      return (
                        <div
                          key={alert.id}
                          className={`p-3 rounded-lg border ${config.bgColor} transition-all`}
                        >
                          <div className="flex items-start gap-3">
                            <div className={`mt-0.5 ${config.iconColor}`}>
                              <Icon className="w-5 h-5" />
                            </div>
                            <div className="flex-1 min-w-0">
                              <div className="flex items-center justify-between gap-2 mb-1">
                                <span className={`text-sm ${config.labelColor}`}>
                                  {config.label}
                                </span>
                                <span className="text-xs text-slate-600 tabular-nums">
                                  {alert.timestamp}
                                </span>
                              </div>
                              <p className="text-sm text-slate-400">
                                {config.description}
                              </p>
                              <p className="text-xs text-slate-600 mt-1">
                                {alert.participant}
                              </p>
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Statistics */}
            <Card className="bg-[#151b2e] border-slate-800/50">
              <CardHeader>
                <CardTitle className="text-slate-100 text-base">통계</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-slate-400">총 참여자</span>
                  <span className="text-lg text-slate-100 tabular-nums">{participants.length}명</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-slate-400">정상</span>
                  <span className="text-lg text-emerald-400 tabular-nums">
                    {participants.filter(p => p.status === "NORMAL").length}명
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-slate-400">졸음</span>
                  <span className="text-lg text-amber-400 tabular-nums">
                    {participants.filter(p => p.status === "DROWSY").length}명
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-slate-400">이탈</span>
                  <span className="text-lg text-red-400 tabular-nums">
                    {participants.filter(p => p.status === "ABSENCE").length}명
                  </span>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
