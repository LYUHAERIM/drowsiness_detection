import { useState, useRef } from "react";
import { useNavigate } from "react-router";
import { ArrowLeft, Upload, Video, Clock, Sparkles, FileVideo } from "lucide-react";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";
import { Progress } from "../components/ui/progress";

export function UploadAnalysis() {
  const navigate = useNavigate();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [classStartTime, setClassStartTime] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [progress, setProgress] = useState(0);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);

    const files = Array.from(e.dataTransfer.files);
    const videoFile = files.find(file => file.type.startsWith("video/"));

    if (videoFile) {
      setUploadedFile(videoFile);
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file && file.type.startsWith("video/")) {
      setUploadedFile(file);
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + " " + sizes[i];
  };

  const handleStartAnalysis = () => {
    if (!uploadedFile || !classStartTime) return;

    setIsAnalyzing(true);
    setProgress(0);

    // Simulate analysis progress
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          setTimeout(() => {
            navigate("/upload/result");
          }, 500);
          return 100;
        }
        return prev + 10;
      });
    }, 500);
  };

  return (
    <div className="min-h-screen bg-[#0a0e1a]">
      {/* Header */}
      <div className="border-b border-slate-800/50 bg-[#151b2e]/80 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4">
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
              <h1 className="text-xl text-slate-50">녹화 영상 분석</h1>
              <p className="text-sm text-slate-500">
                수업 영상을 업로드하여 분석하세요
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        <div className="max-w-5xl mx-auto">
          <div className="grid lg:grid-cols-[1fr_400px] gap-8">
            {/* Left: Upload Area */}
            <div className="space-y-6">
              <Card className="bg-[#151b2e] border-slate-800/50">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-slate-100">
                    <Upload className="w-5 h-5" />
                    영상 업로드
                  </CardTitle>
                  <CardDescription className="text-slate-500">
                    분석할 수업 영상을 드래그하여 올려주세요
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div
                    onDragOver={handleDragOver}
                    onDragLeave={handleDragLeave}
                    onDrop={handleDrop}
                    onClick={() => fileInputRef.current?.click()}
                    className={`
                      border-2 border-dashed rounded-xl p-12 text-center cursor-pointer
                      transition-all duration-200
                      ${
                        isDragging
                          ? "border-purple-500 bg-purple-500/5"
                          : "border-slate-700 hover:border-purple-500/50 hover:bg-slate-900/50"
                      }
                    `}
                  >
                    <input
                      ref={fileInputRef}
                      type="file"
                      accept="video/*"
                      onChange={handleFileSelect}
                      className="hidden"
                    />

                    {uploadedFile ? (
                      <div className="space-y-4">
                        <div className="w-16 h-16 mx-auto bg-purple-500/10 border border-purple-500/20 rounded-full flex items-center justify-center">
                          <FileVideo className="w-8 h-8 text-purple-400" />
                        </div>
                        <div>
                          <p className="text-lg text-slate-100 mb-2">{uploadedFile.name}</p>
                          <p className="text-sm text-slate-500">
                            {formatFileSize(uploadedFile.size)}
                          </p>
                        </div>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={(e) => {
                            e.stopPropagation();
                            setUploadedFile(null);
                          }}
                          className="border-slate-700 text-slate-300 hover:bg-slate-800"
                        >
                          다른 파일 선택
                        </Button>
                      </div>
                    ) : (
                      <div className="space-y-4">
                        <div className="w-16 h-16 mx-auto bg-slate-800/50 rounded-full flex items-center justify-center">
                          <Upload className="w-8 h-8 text-slate-600" />
                        </div>
                        <div>
                          <p className="text-lg text-slate-300 mb-2">
                            영상을 드래그하거나 클릭하여 업로드
                          </p>
                          <p className="text-sm text-slate-600">
                            MP4, AVI, MOV 등의 형식 지원
                          </p>
                        </div>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>

              {/* Analysis Progress */}
              {isAnalyzing && (
                <Card className="bg-[#151b2e] border-slate-800/50">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2 text-slate-100">
                      <Sparkles className="w-5 h-5 text-purple-400" />
                      분석 진행 중
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span className="text-slate-400">
                          AI가 영상을 분석하고 있습니다...
                        </span>
                        <span className="text-slate-100 tabular-nums">
                          {progress}%
                        </span>
                      </div>
                      <Progress value={progress} className="h-2" />
                    </div>
                    <p className="text-xs text-slate-600">
                      영상 길이에 따라 몇 분이 소요될 수 있습니다
                    </p>
                  </CardContent>
                </Card>
              )}
            </div>

            {/* Right: Settings */}
            <div className="space-y-6">
              <Card className="bg-[#151b2e] border-slate-800/50">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-slate-100">
                    <Clock className="w-5 h-5" />
                    수업 정보
                  </CardTitle>
                  <CardDescription className="text-slate-500">
                    분석에 필요한 정보를 입력하세요
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="start-time" className="text-slate-300">수업 시작 시간</Label>
                    <Input
                      id="start-time"
                      type="time"
                      value={classStartTime}
                      onChange={(e) => setClassStartTime(e.target.value)}
                      placeholder="09:00"
                      className="bg-slate-900/50 border-slate-700 text-slate-100"
                    />
                    <p className="text-xs text-slate-600">
                      리포트의 시간 표시에 사용됩니다
                    </p>
                  </div>

                  <Button
                    className="w-full bg-purple-600 hover:bg-purple-700 text-white shadow-lg shadow-purple-600/20"
                    size="lg"
                    disabled={!uploadedFile || !classStartTime || isAnalyzing}
                    onClick={handleStartAnalysis}
                  >
                    <Sparkles className="w-4 h-4 mr-2" />
                    분석 시작
                  </Button>
                </CardContent>
              </Card>

              <Card className="bg-[#151b2e] border-slate-800/50">
                <CardHeader>
                  <CardTitle className="text-base text-slate-100">분석 기능</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="flex items-start gap-3">
                    <div className="w-8 h-8 rounded-lg bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center flex-shrink-0">
                      <Video className="w-4 h-4 text-emerald-400" />
                    </div>
                    <div>
                      <p className="text-sm text-slate-300">얼굴 감지 및 추적</p>
                      <p className="text-xs text-slate-600">
                        모든 참여자의 얼굴을 실시간으로 추적합니다
                      </p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <div className="w-8 h-8 rounded-lg bg-amber-500/10 border border-amber-500/20 flex items-center justify-center flex-shrink-0">
                      <Sparkles className="w-4 h-4 text-amber-400" />
                    </div>
                    <div>
                      <p className="text-sm text-slate-300">졸음 감지</p>
                      <p className="text-xs text-slate-600">
                        눈 깜빡임과 고개 움직임을 분석합니다
                      </p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <div className="w-8 h-8 rounded-lg bg-red-500/10 border border-red-500/20 flex items-center justify-center flex-shrink-0">
                      <Clock className="w-4 h-4 text-red-400" />
                    </div>
                    <div>
                      <p className="text-sm text-slate-300">이탈 감지</p>
                      <p className="text-xs text-slate-600">
                        화면 이탈 시간을 정확히 측정합니다
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-gradient-to-br from-purple-500/5 to-blue-500/5 border-purple-500/20">
                <CardContent className="pt-6">
                  <div className="space-y-2">
                    <p className="text-sm text-slate-300">💡 분석 팁</p>
                    <ul className="text-xs text-slate-500 space-y-1 list-disc list-inside">
                      <li>해상도가 높을수록 정확도가 향상됩니다</li>
                      <li>참여자의 얼굴이 잘 보이는 영상을 업로드하세요</li>
                      <li>1시간 영상 기준 약 5-10분 소요됩니다</li>
                    </ul>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
