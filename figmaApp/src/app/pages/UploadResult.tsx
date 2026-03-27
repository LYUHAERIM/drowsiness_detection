import { useState } from "react";
import { useNavigate } from "react-router";
import { ArrowLeft, Download, Play, Pause, TrendingUp, Users, Clock, AlertTriangle } from "lucide-react";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../components/ui/tabs";
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

export function UploadResult() {
  const navigate = useNavigate();
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const totalDuration = 3720; // 1 hour 2 minutes in seconds

  // Mock data for hourly analysis
  const hourlyData = [
    { time: "9:00", normal: 8, drowsy: 0, absence: 0, focus: 100 },
    { time: "9:15", normal: 7, drowsy: 1, absence: 0, focus: 95 },
    { time: "9:30", normal: 6, drowsy: 2, absence: 0, focus: 85 },
    { time: "9:45", normal: 5, drowsy: 2, absence: 1, focus: 80 },
    { time: "10:00", normal: 7, drowsy: 1, absence: 0, focus: 92 },
    { time: "10:15", normal: 6, drowsy: 1, absence: 1, focus: 88 },
    { time: "10:30", normal: 7, drowsy: 1, absence: 0, focus: 90 },
    { time: "10:45", normal: 8, drowsy: 0, absence: 0, focus: 98 },
  ];

  // Individual student data
  const students = [
    {
      id: 1,
      name: "김민수",
      avatar: "👨",
      totalTime: 62,
      focusTime: 54,
      drowsyTime: 6,
      absenceTime: 2,
      focusRate: 87,
      drowsyEvents: 8,
      absenceEvents: 2,
    },
    {
      id: 2,
      name: "이서연",
      avatar: "👩",
      totalTime: 62,
      focusTime: 58,
      drowsyTime: 3,
      absenceTime: 1,
      focusRate: 94,
      drowsyEvents: 4,
      absenceEvents: 1,
    },
    {
      id: 3,
      name: "박지훈",
      avatar: "👨",
      totalTime: 62,
      focusTime: 51,
      drowsyTime: 9,
      absenceTime: 2,
      focusRate: 82,
      drowsyEvents: 12,
      absenceEvents: 3,
    },
    {
      id: 4,
      name: "최유진",
      avatar: "👩",
      totalTime: 62,
      focusTime: 56,
      drowsyTime: 4,
      absenceTime: 2,
      focusRate: 90,
      drowsyEvents: 5,
      absenceEvents: 2,
    },
    {
      id: 5,
      name: "정태양",
      avatar: "👨",
      totalTime: 62,
      focusTime: 59,
      drowsyTime: 2,
      absenceTime: 1,
      focusRate: 95,
      drowsyEvents: 3,
      absenceEvents: 1,
    },
    {
      id: 6,
      name: "강민지",
      avatar: "👩",
      totalTime: 62,
      focusTime: 55,
      drowsyTime: 5,
      absenceTime: 2,
      focusRate: 89,
      drowsyEvents: 6,
      absenceEvents: 2,
    },
    {
      id: 7,
      name: "윤성호",
      avatar: "👨",
      totalTime: 62,
      focusTime: 52,
      drowsyTime: 7,
      absenceTime: 3,
      focusRate: 84,
      drowsyEvents: 9,
      absenceEvents: 3,
    },
    {
      id: 8,
      name: "한지아",
      avatar: "👩",
      totalTime: 62,
      focusTime: 57,
      drowsyTime: 4,
      absenceTime: 1,
      focusRate: 92,
      drowsyEvents: 5,
      absenceEvents: 1,
    },
  ];

  const formatTime = (seconds: number) => {
    const hours = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hours}:${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
  };

  const getFocusColor = (rate: number) => {
    if (rate >= 90) return "text-emerald-400";
    if (rate >= 80) return "text-amber-400";
    return "text-red-400";
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
                onClick={() => navigate("/upload")}
                className="text-slate-400 hover:text-slate-100 hover:bg-slate-800"
              >
                <ArrowLeft className="w-5 h-5" />
              </Button>
              <div>
                <h1 className="text-xl text-slate-50">영상 분석 결과</h1>
                <p className="text-sm text-slate-500">
                  2026-03-26 09:00 수업 (1시간 2분)
                </p>
              </div>
            </div>
            <div className="flex gap-2">
              <Button variant="outline" className="border-slate-700 text-slate-300 hover:bg-slate-800">
                <Download className="w-4 h-4 mr-2" />
                PDF
              </Button>
              <Button variant="outline" className="border-slate-700 text-slate-300 hover:bg-slate-800">
                <Download className="w-4 h-4 mr-2" />
                Excel
              </Button>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        <div className="max-w-7xl mx-auto space-y-6">
          {/* Summary Cards */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <Card className="bg-[#151b2e] border-slate-800/50">
              <CardHeader className="pb-3">
                <CardDescription className="flex items-center gap-2 text-slate-500">
                  <Users className="w-4 h-4" />
                  총 참여자
                </CardDescription>
                <CardTitle className="text-3xl text-slate-100 tabular-nums">8명</CardTitle>
              </CardHeader>
            </Card>
            <Card className="bg-[#151b2e] border-slate-800/50">
              <CardHeader className="pb-3">
                <CardDescription className="flex items-center gap-2 text-slate-500">
                  <TrendingUp className="w-4 h-4" />
                  평균 집중도
                </CardDescription>
                <CardTitle className="text-3xl text-emerald-400 tabular-nums">89.1%</CardTitle>
              </CardHeader>
            </Card>
            <Card className="bg-[#151b2e] border-slate-800/50">
              <CardHeader className="pb-3">
                <CardDescription className="flex items-center gap-2 text-slate-500">
                  <AlertTriangle className="w-4 h-4" />
                  총 졸음 감지
                </CardDescription>
                <CardTitle className="text-3xl text-amber-400 tabular-nums">52회</CardTitle>
              </CardHeader>
            </Card>
            <Card className="bg-[#151b2e] border-slate-800/50">
              <CardHeader className="pb-3">
                <CardDescription className="flex items-center gap-2 text-slate-500">
                  <Clock className="w-4 h-4" />
                  총 이탈 감지
                </CardDescription>
                <CardTitle className="text-3xl text-red-400 tabular-nums">15회</CardTitle>
              </CardHeader>
            </Card>
          </div>

          {/* Video Player */}
          <Card className="bg-[#151b2e] border-slate-800/50">
            <CardHeader>
              <CardTitle className="text-slate-100">분석 영상</CardTitle>
              <CardDescription className="text-slate-500">
                타임라인에서 특정 구간을 클릭하여 바로 이동할 수 있습니다
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="aspect-video bg-slate-950/50 rounded-lg relative overflow-hidden">
                <div className="absolute inset-0 flex items-center justify-center">
                  <img
                    src="figma:asset/80652276761e4f9c48177aee51bd30dc4ad0897a.png"
                    alt="Analyzed video"
                    className="w-full h-full object-cover"
                  />
                </div>

                {/* Video Controls */}
                <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-slate-900 to-transparent p-4">
                  <div className="space-y-2">
                    <div className="h-2 bg-slate-800 rounded-full overflow-hidden cursor-pointer">
                      <div
                        className="h-full bg-purple-500"
                        style={{ width: `${(currentTime / totalDuration) * 100}%` }}
                      />
                    </div>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <Button
                          size="sm"
                          variant="ghost"
                          className="text-slate-100 hover:bg-slate-800"
                          onClick={() => setIsPlaying(!isPlaying)}
                        >
                          {isPlaying ? (
                            <Pause className="w-5 h-5" />
                          ) : (
                            <Play className="w-5 h-5" />
                          )}
                        </Button>
                        <span className="text-sm text-slate-100 tabular-nums">
                          {formatTime(currentTime)} / {formatTime(totalDuration)}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Charts and Analysis */}
          <Tabs defaultValue="timeline" className="space-y-4">
            <TabsList className="grid w-full md:w-auto md:inline-grid grid-cols-3 bg-[#151b2e] border-slate-800/50">
              <TabsTrigger value="timeline">시간대별 분석</TabsTrigger>
              <TabsTrigger value="students">학생별 분석</TabsTrigger>
              <TabsTrigger value="insights">인사이트</TabsTrigger>
            </TabsList>

            <TabsContent value="timeline" className="space-y-4">
              <Card className="bg-[#151b2e] border-slate-800/50">
                <CardHeader>
                  <CardTitle className="text-slate-100">시간대별 집중도 추이</CardTitle>
                  <CardDescription className="text-slate-500">
                    수업 진행에 따른 학생들의 집중도 변화
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={hourlyData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                      <XAxis dataKey="time" stroke="#64748b" tick={{ fill: '#94a3b8' }} />
                      <YAxis stroke="#64748b" tick={{ fill: '#94a3b8' }} />
                      <Tooltip
                        contentStyle={{
                          backgroundColor: '#1e293b',
                          border: '1px solid #334155',
                          borderRadius: '8px',
                          color: '#e2e8f0',
                        }}
                      />
                      <Legend wrapperStyle={{ color: '#94a3b8' }} />
                      <Line
                        type="monotone"
                        dataKey="focus"
                        stroke="#a855f7"
                        strokeWidth={2}
                        name="평균 집중도 (%)"
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              <Card className="bg-[#151b2e] border-slate-800/50">
                <CardHeader>
                  <CardTitle className="text-slate-100">참여자 상태 분포</CardTitle>
                  <CardDescription className="text-slate-500">
                    시간대별 정상/졸음/이탈 참여자 수
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <AreaChart data={hourlyData}>
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
                      <XAxis dataKey="time" stroke="#64748b" tick={{ fill: '#94a3b8' }} />
                      <YAxis stroke="#64748b" tick={{ fill: '#94a3b8' }} />
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
            </TabsContent>

            <TabsContent value="students" className="space-y-4">
              <Card className="bg-[#151b2e] border-slate-800/50">
                <CardHeader>
                  <CardTitle className="text-slate-100">학생별 집중도 비교</CardTitle>
                  <CardDescription className="text-slate-500">
                    각 학생의 집중도를 한눈에 비교
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={students}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                      <XAxis dataKey="name" stroke="#64748b" tick={{ fill: '#94a3b8' }} />
                      <YAxis stroke="#64748b" tick={{ fill: '#94a3b8' }} />
                      <Tooltip
                        contentStyle={{
                          backgroundColor: '#1e293b',
                          border: '1px solid #334155',
                          borderRadius: '8px',
                          color: '#e2e8f0',
                        }}
                      />
                      <Legend wrapperStyle={{ color: '#94a3b8' }} />
                      <Bar dataKey="focusRate" fill="#a855f7" name="집중도 (%)" />
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              <div className="grid gap-4">
                {students.map((student) => (
                  <Card key={student.id} className="bg-[#151b2e] border-slate-800/50">
                    <CardContent className="pt-6">
                      <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center gap-3">
                          <div className="w-12 h-12 rounded-full bg-gradient-to-br from-purple-500/20 to-blue-500/20 border border-purple-500/30 flex items-center justify-center text-2xl">
                            {student.avatar}
                          </div>
                          <div>
                            <h3 className="text-lg text-slate-100">{student.name}</h3>
                            <p className="text-sm text-slate-500">
                              참여 시간: {student.totalTime}분
                            </p>
                          </div>
                        </div>
                        <div className="text-right">
                          <p className={`text-3xl tabular-nums ${getFocusColor(student.focusRate)}`}>
                            {student.focusRate}%
                          </p>
                          <p className="text-sm text-slate-500">
                            집중도
                          </p>
                        </div>
                      </div>

                      <div className="space-y-3">
                        <div className="flex gap-0.5 h-3 rounded-full overflow-hidden bg-slate-900/50">
                          <div
                            className="bg-emerald-500"
                            style={{ width: `${(student.focusTime / student.totalTime) * 100}%` }}
                          />
                          <div
                            className="bg-amber-500"
                            style={{ width: `${(student.drowsyTime / student.totalTime) * 100}%` }}
                          />
                          <div
                            className="bg-red-500"
                            style={{ width: `${(student.absenceTime / student.totalTime) * 100}%` }}
                          />
                        </div>

                        <div className="grid grid-cols-3 gap-4 text-sm">
                          <div>
                            <p className="text-slate-500">집중</p>
                            <p className="text-lg text-slate-100 tabular-nums">{student.focusTime}분</p>
                          </div>
                          <div>
                            <p className="text-slate-500">졸음</p>
                            <p className="text-lg text-amber-400 tabular-nums">
                              {student.drowsyTime}분 ({student.drowsyEvents}회)
                            </p>
                          </div>
                          <div>
                            <p className="text-slate-500">이탈</p>
                            <p className="text-lg text-red-400 tabular-nums">
                              {student.absenceTime}분 ({student.absenceEvents}회)
                            </p>
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            <TabsContent value="insights" className="space-y-4">
              <Card className="bg-[#151b2e] border-slate-800/50">
                <CardHeader>
                  <CardTitle className="text-slate-100">주요 발견 사항</CardTitle>
                  <CardDescription className="text-slate-500">
                    AI가 분석한 수업 집중도 인사이트
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex gap-3 p-4 bg-emerald-500/5 rounded-lg border border-emerald-500/20">
                    <TrendingUp className="w-5 h-5 text-emerald-400 flex-shrink-0 mt-0.5" />
                    <div>
                      <h4 className="mb-1 text-slate-200">높은 전체 집중도</h4>
                      <p className="text-sm text-slate-400">
                        전체 평균 집중도가 89.1%로 매우 우수합니다. 특히 정태양, 이서연 학생이 95%, 94%의 높은 집중도를 보였습니다.
                      </p>
                    </div>
                  </div>

                  <div className="flex gap-3 p-4 bg-amber-500/5 rounded-lg border border-amber-500/20">
                    <AlertTriangle className="w-5 h-5 text-amber-400 flex-shrink-0 mt-0.5" />
                    <div>
                      <h4 className="mb-1 text-slate-200">중반부 집중도 저하</h4>
                      <p className="text-sm text-slate-400">
                        9:30~9:45 구간에서 집중도가 80%로 하락했습니다. 이 시간대에 짧은 휴식이나 인터랙티브 활동을 추천합니다.
                      </p>
                    </div>
                  </div>

                  <div className="flex gap-3 p-4 bg-blue-500/5 rounded-lg border border-blue-500/20">
                    <Users className="w-5 h-5 text-blue-400 flex-shrink-0 mt-0.5" />
                    <div>
                      <h4 className="mb-1 text-slate-200">개별 학생 지원 필요</h4>
                      <p className="text-sm text-slate-400">
                        박지훈 학생의 집중도가 82%로 다른 학생들에 비해 낮습니다. 개별 면담이나 추가 지원이 필요할 수 있습니다.
                      </p>
                    </div>
                  </div>

                  <div className="flex gap-3 p-4 bg-purple-500/5 rounded-lg border border-purple-500/20">
                    <Clock className="w-5 h-5 text-purple-400 flex-shrink-0 mt-0.5" />
                    <div>
                      <h4 className="mb-1 text-slate-200">수업 후반 집중도 회복</h4>
                      <p className="text-sm text-slate-400">
                        10:30 이후 집중도가 다시 상승하여 98%에 도달했습니다. 효과적인 수업 마무리 전략이 작용한 것으로 보입니다.
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-[#151b2e] border-slate-800/50">
                <CardHeader>
                  <CardTitle className="text-slate-100">개선 제안</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="flex items-start gap-3">
                    <Badge className="bg-purple-600/20 text-purple-300 border-purple-500/30 mt-1">1</Badge>
                    <p className="text-sm text-slate-300">
                      수업 중반(30-45분 경과 시점)에 5분 정도의 짧은 휴식 시간을 도입하세요.
                    </p>
                  </div>
                  <div className="flex items-start gap-3">
                    <Badge className="bg-purple-600/20 text-purple-300 border-purple-500/30 mt-1">2</Badge>
                    <p className="text-sm text-slate-300">
                      집중도가 낮은 학생들을 위해 인터랙티브한 질문이나 퀴즈를 활용하세요.
                    </p>
                  </div>
                  <div className="flex items-start gap-3">
                    <Badge className="bg-purple-600/20 text-purple-300 border-purple-500/30 mt-1">3</Badge>
                    <p className="text-sm text-slate-300">
                      개별 학생의 학습 패턴을 파악하여 맞춤형 지원을 제공하세요.
                    </p>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  );
}
