import { useNavigate } from "react-router";
import { ArrowLeft, Download, TrendingUp, AlertCircle, Clock, Circle, AlertTriangle, CircleDot } from "lucide-react";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

export function RealtimeReport() {
  const navigate = useNavigate();

  // Mock data for time-series chart
  const timeSeriesData = [
    { time: "0:00", normal: 5, drowsy: 0, absence: 0 },
    { time: "0:15", normal: 5, drowsy: 0, absence: 0 },
    { time: "0:30", normal: 4, drowsy: 1, absence: 0 },
    { time: "0:45", normal: 3, drowsy: 2, absence: 0 },
    { time: "1:00", normal: 4, drowsy: 1, absence: 0 },
    { time: "1:15", normal: 3, drowsy: 1, absence: 1 },
    { time: "1:30", normal: 4, drowsy: 1, absence: 0 },
    { time: "1:45", normal: 5, drowsy: 0, absence: 0 },
    { time: "2:00", normal: 5, drowsy: 0, absence: 0 },
  ];

  // Mock event log data
  const eventLogs = [
    { id: 1, time: "1:23", participant: "김주원", event: "drowsy" },
    { id: 2, time: "1:15", participant: "조인선", event: "absence" },
    { id: 3, time: "0:58", participant: "박해슬", event: "drowsy" },
    { id: 4, time: "0:45", participant: "김태완", event: "drowsy" },
    { id: 5, time: "0:32", participant: "김주원", event: "drowsy" },
  ];

  // Summary statistics
  const participants = [
    { name: "강경미", normal: 95, drowsy: 5, absence: 0, focus: 95 },
    { name: "박해슬", normal: 85, drowsy: 12, absence: 3, focus: 85 },
    { name: "김주원 (나)", normal: 78, drowsy: 18, absence: 4, focus: 78 },
    { name: "조인선", normal: 88, drowsy: 8, absence: 4, focus: 88 },
    { name: "김태완", normal: 92, drowsy: 8, absence: 0, focus: 92 },
  ];

  const getEventConfig = (type: string) => {
    switch (type) {
      case "drowsy":
        return {
          icon: AlertTriangle,
          label: "졸음",
          description: "졸음이 감지되었습니다",
          bgColor: "bg-amber-500/5 border-amber-500/20",
          iconColor: "text-amber-400",
        };
      case "absence":
        return {
          icon: Circle,
          label: "이탈",
          description: "자리를 이탈했습니다",
          bgColor: "bg-red-500/5 border-red-500/20",
          iconColor: "text-red-400",
        };
      default:
        return {
          icon: CircleDot,
          label: "정상",
          description: "수업에 집중하고 있습니다",
          bgColor: "bg-emerald-500/5 border-emerald-500/20",
          iconColor: "text-emerald-400",
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
                onClick={() => navigate("/realtime")}
                className="text-slate-400 hover:text-slate-100 hover:bg-slate-800"
              >
                <ArrowLeft className="w-5 h-5" />
              </Button>
              <div>
                <h1 className="text-xl text-slate-50">실시간 분석 리포트</h1>
                <p className="text-sm text-slate-500">
                  2분 데모 영상 분석 결과
                </p>
              </div>
            </div>
            <Button variant="outline" className="border-slate-700 text-slate-300 hover:bg-slate-800">
              <Download className="w-4 h-4 mr-2" />
              리포트 다운로드
            </Button>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        <div className="max-w-7xl mx-auto space-y-6">
          {/* Summary Cards */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <Card className="bg-[#151b2e] border-slate-800/50">
              <CardHeader className="pb-3">
                <CardDescription className="text-slate-500">총 참여자</CardDescription>
                <CardTitle className="text-3xl text-slate-100 tabular-nums">5명</CardTitle>
              </CardHeader>
            </Card>
            <Card className="bg-[#151b2e] border-slate-800/50">
              <CardHeader className="pb-3">
                <CardDescription className="text-slate-500">평균 집중도</CardDescription>
                <CardTitle className="text-3xl text-emerald-400 tabular-nums">87.6%</CardTitle>
              </CardHeader>
            </Card>
            <Card className="bg-[#151b2e] border-slate-800/50">
              <CardHeader className="pb-3">
                <CardDescription className="text-slate-500">졸음 감지</CardDescription>
                <CardTitle className="text-3xl text-amber-400 tabular-nums">4회</CardTitle>
              </CardHeader>
            </Card>
            <Card className="bg-[#151b2e] border-slate-800/50">
              <CardHeader className="pb-3">
                <CardDescription className="text-slate-500">이탈 감지</CardDescription>
                <CardTitle className="text-3xl text-red-400 tabular-nums">1회</CardTitle>
              </CardHeader>
            </Card>
          </div>

          {/* Time-series Chart */}
          <Card className="bg-[#151b2e] border-slate-800/50">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-slate-100">
                <TrendingUp className="w-5 h-5" />
                시간대별 상태 분석
              </CardTitle>
              <CardDescription className="text-slate-500">
                2분 동안의 참여자 상태 변화 추이
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <AreaChart data={timeSeriesData}>
                  <defs>
                    <linearGradient id="colorNormal" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                    </linearGradient>
                    <linearGradient id="colorDrowsy" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#f59e0b" stopOpacity={0}/>
                    </linearGradient>
                    <linearGradient id="colorAbsence" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#ef4444" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                  <XAxis
                    dataKey="time"
                    stroke="#64748b"
                    tick={{ fill: '#94a3b8' }}
                  />
                  <YAxis
                    stroke="#64748b"
                    tick={{ fill: '#94a3b8' }}
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#1e293b',
                      border: '1px solid #334155',
                      borderRadius: '8px',
                      color: '#e2e8f0',
                    }}
                  />
                  <Legend wrapperStyle={{ color: '#94a3b8' }} />
                  <Area
                    type="monotone"
                    dataKey="normal"
                    stackId="1"
                    stroke="#10b981"
                    fill="url(#colorNormal)"
                    strokeWidth={2}
                    name="정상"
                  />
                  <Area
                    type="monotone"
                    dataKey="drowsy"
                    stackId="1"
                    stroke="#f59e0b"
                    fill="url(#colorDrowsy)"
                    strokeWidth={2}
                    name="졸음"
                  />
                  <Area
                    type="monotone"
                    dataKey="absence"
                    stackId="1"
                    stroke="#ef4444"
                    fill="url(#colorAbsence)"
                    strokeWidth={2}
                    name="이탈"
                  />
                </AreaChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          <div className="grid lg:grid-cols-2 gap-6">
            {/* Event Log */}
            <Card className="bg-[#151b2e] border-slate-800/50">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-slate-100">
                  <AlertCircle className="w-5 h-5" />
                  이벤트 로그
                </CardTitle>
                <CardDescription className="text-slate-500">졸음 및 이탈 발생 시점</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {eventLogs.map((log) => {
                    const config = getEventConfig(log.event);
                    const Icon = config.icon;

                    return (
                      <div
                        key={log.id}
                        className={`p-3 rounded-lg border ${config.bgColor}`}
                      >
                        <div className="flex items-start gap-3">
                          <div className={`mt-0.5 ${config.iconColor}`}>
                            <Icon className="w-5 h-5" />
                          </div>
                          <div className="flex-1">
                            <div className="flex items-center justify-between gap-2 mb-1">
                              <span className={`text-sm ${config.iconColor}`}>
                                {config.label}
                              </span>
                              <Badge variant="outline" className="text-xs text-slate-500 border-slate-700 tabular-nums">
                                {log.time}
                              </Badge>
                            </div>
                            <p className="text-sm text-slate-400">
                              {config.description}
                            </p>
                            <p className="text-xs text-slate-600 mt-1">
                              {log.participant}
                            </p>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </CardContent>
            </Card>

            {/* Participant Summary */}
            <Card className="bg-[#151b2e] border-slate-800/50">
              <CardHeader>
                <CardTitle className="text-slate-100">참여자별 통계</CardTitle>
                <CardDescription className="text-slate-500">개인별 집중도 및 상태 분석</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {participants.map((participant, idx) => (
                    <div key={idx} className="space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-slate-300">{participant.name}</span>
                        <span className="text-sm text-slate-500 tabular-nums">
                          집중도 {participant.focus}%
                        </span>
                      </div>
                      <div className="flex gap-0.5 h-2 rounded-full overflow-hidden bg-slate-900/50">
                        <div
                          className="bg-emerald-500"
                          style={{ width: `${participant.normal}%` }}
                        />
                        <div
                          className="bg-amber-500"
                          style={{ width: `${participant.drowsy}%` }}
                        />
                        <div
                          className="bg-red-500"
                          style={{ width: `${participant.absence}%` }}
                        />
                      </div>
                      <div className="flex gap-4 text-xs text-slate-600">
                        <span>정상 {participant.normal}%</span>
                        <span>졸음 {participant.drowsy}%</span>
                        <span>이탈 {participant.absence}%</span>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Recommendations */}
          <Card className="bg-[#151b2e] border-slate-800/50">
            <CardHeader>
              <CardTitle className="text-slate-100">분석 결과 및 제안</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex gap-3 p-4 bg-blue-500/5 rounded-lg border border-blue-500/20">
                <TrendingUp className="w-5 h-5 text-blue-400 flex-shrink-0 mt-0.5" />
                <div>
                  <p className="text-sm text-slate-300">
                    전체적으로 높은 집중도를 보이고 있습니다. 평균 87.6%의 집중도를 유지했습니다.
                  </p>
                </div>
              </div>
              <div className="flex gap-3 p-4 bg-amber-500/5 rounded-lg border border-amber-500/20">
                <AlertCircle className="w-5 h-5 text-amber-400 flex-shrink-0 mt-0.5" />
                <div>
                  <p className="text-sm text-slate-300">
                    김주원 학생의 경우 0:30~1:00 구간에서 졸음 상태가 자주 감지되었습니다. 해당 시간대에 휴식 시간을 권장합니다.
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
