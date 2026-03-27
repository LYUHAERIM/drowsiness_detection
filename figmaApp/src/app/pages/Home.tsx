import { useNavigate } from "react-router";
import { Video, Upload, Zap, Clock, Activity } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { Button } from "../components/ui/button";

export function Home() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-[#0a0e1a]">
      {/* Background Pattern */}
      <div className="fixed inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(17,24,39,0.5),transparent_50%)] pointer-events-none" />

      <div className="relative container mx-auto px-4 py-16">
        <div className="max-w-6xl mx-auto">
          {/* Header */}
          <div className="text-center mb-16">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-blue-500/10 border border-blue-500/20 mb-6">
              <Activity className="w-4 h-4 text-blue-400" />
              <span className="text-sm text-blue-300">AI-Powered Monitoring System</span>
            </div>
            <h1 className="text-5xl mb-4 text-slate-50 tracking-tight">
              AI 수업 집중도 분석 시스템
            </h1>
            <p className="text-xl text-slate-400">
              온라인 수업에서 졸음 및 이탈 상태를 실시간으로 모니터링합니다
            </p>
          </div>

          {/* Mode Selection Cards */}
          <div className="grid md:grid-cols-2 gap-6 max-w-5xl mx-auto">
            {/* Real-time Demo Card */}
            <Card className="bg-[#151b2e] border-slate-800 hover:border-blue-500/50 hover:shadow-lg hover:shadow-blue-500/10 transition-all cursor-pointer group">
              <CardHeader>
                <div className="w-14 h-14 bg-blue-500/10 border border-blue-500/20 rounded-xl flex items-center justify-center mb-4 group-hover:bg-blue-500/20 transition-all">
                  <Video className="w-7 h-7 text-blue-400" />
                </div>
                <CardTitle className="text-2xl text-slate-50">실시간 분석</CardTitle>
                <CardDescription className="text-base text-slate-400">Demo Mode</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <p className="text-slate-300">
                  2분 데모 영상에 내 웹캠을 오버레이하여 실시간 분석
                </p>

                <div className="space-y-3">
                  <div className="flex items-start gap-3">
                    <div className="w-8 h-8 rounded-lg bg-blue-500/10 flex items-center justify-center flex-shrink-0 mt-0.5">
                      <Zap className="w-4 h-4 text-blue-400" />
                    </div>
                    <div>
                      <p className="text-sm text-slate-200">
                        실시간 상태 표시
                      </p>
                      <p className="text-xs text-slate-500">
                        졸음, 이탈 상태를 즉시 감지
                      </p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <div className="w-8 h-8 rounded-lg bg-blue-500/10 flex items-center justify-center flex-shrink-0 mt-0.5">
                      <Video className="w-4 h-4 text-blue-400" />
                    </div>
                    <div>
                      <p className="text-sm text-slate-200">
                        웹캠 오버레이
                      </p>
                      <p className="text-xs text-slate-500">
                        데모 영상에 나를 합성하여 분석
                      </p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <div className="w-8 h-8 rounded-lg bg-blue-500/10 flex items-center justify-center flex-shrink-0 mt-0.5">
                      <Clock className="w-4 h-4 text-blue-400" />
                    </div>
                    <div>
                      <p className="text-sm text-slate-200">
                        빠른 데모 체험
                      </p>
                      <p className="text-xs text-slate-500">
                        2분 안에 기능 확인
                      </p>
                    </div>
                  </div>
                </div>

                <Button
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white shadow-lg shadow-blue-600/20"
                  size="lg"
                  onClick={() => navigate("/realtime")}
                >
                  실시간 분석 시작
                </Button>
              </CardContent>
            </Card>

            {/* Upload Mode Card */}
            <Card className="bg-[#151b2e] border-slate-800 hover:border-purple-500/50 hover:shadow-lg hover:shadow-purple-500/10 transition-all cursor-pointer group">
              <CardHeader>
                <div className="w-14 h-14 bg-purple-500/10 border border-purple-500/20 rounded-xl flex items-center justify-center mb-4 group-hover:bg-purple-500/20 transition-all">
                  <Upload className="w-7 h-7 text-purple-400" />
                </div>
                <CardTitle className="text-2xl text-slate-50">녹화 영상 분석</CardTitle>
                <CardDescription className="text-base text-slate-400">Upload Mode</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <p className="text-slate-300">
                  긴 수업 영상을 업로드하여 분석 리포트 생성
                </p>

                <div className="space-y-3">
                  <div className="flex items-start gap-3">
                    <div className="w-8 h-8 rounded-lg bg-purple-500/10 flex items-center justify-center flex-shrink-0 mt-0.5">
                      <Upload className="w-4 h-4 text-purple-400" />
                    </div>
                    <div>
                      <p className="text-sm text-slate-200">
                        영상 업로드
                      </p>
                      <p className="text-xs text-slate-500">
                        1시간 이상의 긴 수업 영상 지원
                      </p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <div className="w-8 h-8 rounded-lg bg-purple-500/10 flex items-center justify-center flex-shrink-0 mt-0.5">
                      <Zap className="w-4 h-4 text-purple-400" />
                    </div>
                    <div>
                      <p className="text-sm text-slate-200">
                        상세 리포트
                      </p>
                      <p className="text-xs text-slate-500">
                        시간대별 분석 그래프 및 통계
                      </p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <div className="w-8 h-8 rounded-lg bg-purple-500/10 flex items-center justify-center flex-shrink-0 mt-0.5">
                      <Clock className="w-4 h-4 text-purple-400" />
                    </div>
                    <div>
                      <p className="text-sm text-slate-200">
                        비실시간 분석
                      </p>
                      <p className="text-xs text-slate-500">
                        완료 후 종합 리포트 제공
                      </p>
                    </div>
                  </div>
                </div>

                <Button
                  className="w-full bg-purple-600 hover:bg-purple-700 text-white shadow-lg shadow-purple-600/20"
                  size="lg"
                  onClick={() => navigate("/upload")}
                >
                  영상 업로드하기
                </Button>
              </CardContent>
            </Card>
          </div>

          {/* Footer Info */}
          <div className="mt-16 text-center">
            <p className="text-sm text-slate-600">
              AI 기반 실시간 졸음 감지 및 이탈 분석 시스템
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
