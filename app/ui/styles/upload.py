from textwrap import dedent


def build_upload_css() -> str:
    return dedent(
        """
        #upload-view,
        #upload-view::before,
        #upload-view::after,
        #upload-view > .gr-block,
        #upload-view > .gr-block::before,
        #upload-view > .gr-block::after,
        #upload-view > .gr-block > .gr-block,
        #upload-view > .gr-block > .gr-block::before,
        #upload-view > .gr-block > .gr-block::after,
        #upload-view .gr-group,
        #upload-view .gr-group::before,
        #upload-view .gr-group::after,
        #upload-view .gr-box,
        #upload-view .gr-box::before,
        #upload-view .gr-box::after,
        #upload-view .gr-panel,
        #upload-view .gr-panel::before,
        #upload-view .gr-panel::after,
        #upload-view .block,
        #upload-view .block::before,
        #upload-view .block::after,
        #upload-view .gradio-html,
        #upload-view .gr-row,
        #upload-view .gr-column,
        #upload-view .column,
        #upload-view .html-container,
        #upload-view .prose,
        #upload-page-inner,
        #upload-page-inner::before,
        #upload-page-inner::after,
        #upload-page-inner > .gr-block,
        #upload-page-inner > .gr-block::before,
        #upload-page-inner > .gr-block::after {
            margin: 0 !important;
            padding: 0 !important;
            min-height: 0 !important;
            border: none !important;
            box-shadow: none !important;
            background: #040b1d !important;
            border-color: #040b1d !important;
            outline: none !important;
        }

        #upload-shell-header,
        #upload-layout-wrap,
        #upload-main-column,
        #upload-side-column,
        #upload-upload-card-block,
        #upload-info-card-block,
        #upload-feature-block,
        #upload-file-state-block,
        #upload-tip-block,
        #upload-status-markdown {
            margin: 0 !important;
            padding: 0 !important;
            min-height: 0 !important;
            border: none !important;
            box-shadow: none !important;
            background: transparent !important;
        }

        #upload-view.hide,
        #upload-view.hidden,
        #upload-view .hide,
        #upload-view .hidden {
            display: none !important;
            height: 0 !important;
            min-height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            overflow: hidden !important;
            border: none !important;
        }

        .upload-page-shell {
            background:
                radial-gradient(circle at 50% 0%, rgba(17, 24, 39, 0.55), transparent 48%),
                linear-gradient(180deg, #091122 0%, #040b1d 100%) !important;
            border: 1px solid #040b1d !important;
            border-color: #040b1d !important;
            box-shadow: none !important;
            outline: none !important;
        }

        .upload-page-shell > .gr-block,
        .upload-page-shell > .gr-block > .gr-block,
        .upload-page-inner,
        .upload-page-inner > .gr-block {
            background: #040b1d !important;
            border: 1px solid #040b1d !important;
            border-color: #040b1d !important;
            box-shadow: none !important;
            outline: none !important;
        }

        .upload-page-inner {
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .upload-layout {
            width: min(1280px, calc(100vw - 40px)) !important;
            margin: 0 auto !important;
            padding: 28px 0 100px !important;
            display: grid !important;
            grid-template-columns: minmax(0, 1.2fr) minmax(340px, 0.82fr);
            gap: 28px !important;
            align-items: start !important;
            background: transparent !important;
        }

        #upload-shell-header {
            width: min(1280px, calc(100vw - 40px)) !important;
            margin: 0 auto !important;
        }

        #upload-view .upload-layout > .gr-block {
            min-width: 0 !important;
        }

        .upload-main-column,
        .upload-side-column {
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            gap: 22px !important;
            background: transparent !important;
        }

        .upload-main-column > .gr-block,
        .upload-side-column > .gr-block,
        .upload-upload-card,
        .upload-info-card {
            width: 100% !important;
        }

        .upload-panel-card,
        .upload-feature-card,
        .upload-tip-card,
        .upload-upload-card,
        .upload-info-card {
            background: rgba(17, 27, 58, 0.92) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 22px !important;
            box-shadow: 0 16px 40px rgba(0, 0, 0, 0.26) !important;
        }

        .upload-panel-card {
            padding: 22px 22px 18px !important;
        }

        .upload-upload-card,
        .upload-info-card {
            padding: 0 22px 22px !important;
        }

        .upload-card-head {
            display: flex;
            align-items: flex-start;
            gap: 14px;
        }

        .upload-card-icon {
            width: 44px;
            height: 44px;
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            flex-shrink: 0;
        }

        .upload-card-icon-upload {
            background: rgba(59, 130, 246, 0.12);
            color: #c7d2fe;
            border: 1px solid rgba(96, 165, 250, 0.22);
        }

        .upload-card-icon-time {
            background: rgba(124, 58, 237, 0.14);
            color: #ddd6fe;
            border: 1px solid rgba(167, 139, 250, 0.22);
        }

        .upload-card-copy h3 {
            margin: 0;
            color: #f8fafc;
            font-size: 28px;
            font-weight: 800;
            letter-spacing: -0.03em;
        }

        .upload-card-copy p {
            margin: 6px 0 0;
            color: rgba(226, 232, 240, 0.72);
            font-size: 15px;
            line-height: 1.6;
        }

        .upload-time-field-label {
            margin-top: 18px;
            color: #e2e8f0;
            font-size: 15px;
            font-weight: 700;
        }

        .upload-file-state {
            margin-top: 18px;
            margin-bottom: 16px;
            padding: 16px 18px;
            border-radius: 16px;
            background: rgba(37, 99, 235, 0.10);
            border: 1px solid rgba(96, 165, 250, 0.18);
        }

        .upload-file-empty {
            background: rgba(15, 23, 42, 0.54);
            border-color: rgba(255, 255, 255, 0.08);
        }

        .upload-file-state-title {
            color: #f8fafc;
            font-size: 16px;
            font-weight: 700;
        }

        .upload-file-state-copy {
            margin-top: 4px;
            color: rgba(226, 232, 240, 0.68);
            font-size: 13px;
        }

        .upload-file {
            min-height: 270px;
            padding: 0 !important;
            background: transparent !important;
            border: none !important;
        }

        .upload-file > .gr-block,
        .upload-file .gr-group,
        .upload-file .gr-box,
        .upload-file .gr-panel,
        .upload-file .block {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }

        .upload-file .wrap,
        .upload-file .file-upload,
        .upload-file [data-testid="file-upload"],
        .upload-file .center,
        .upload-file .file-preview,
        .upload-file label {
            background: transparent !important;
        }

        .figma-upload-input {
            border: 2px dashed rgba(148, 163, 184, 0.28) !important;
            border-radius: 18px !important;
            background: rgba(20, 30, 62, 0.84) !important;
            min-height: 250px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            padding: 22px !important;
        }

        .figma-upload-input:hover {
            border-color: rgba(167, 139, 250, 0.45) !important;
            background: rgba(22, 33, 68, 0.96) !important;
        }

        .upload-file .icon,
        .upload-file svg {
            width: 34px !important;
            height: 34px !important;
        }

        .upload-file .text,
        .upload-file span,
        .upload-file p {
            color: #f8fafc !important;
            font-size: 17px !important;
            line-height: 1.7 !important;
            text-align: center !important;
        }

        .upload-file button {
            border-radius: 14px !important;
            background: rgba(124, 58, 237, 0.16) !important;
            border: 1px solid rgba(167, 139, 250, 0.22) !important;
            color: #e9d5ff !important;
        }

        .upload-status-markdown,
        .upload-status-markdown p {
            margin: 16px 0 0 !important;
            color: #e2e8f0 !important;
            line-height: 1.7 !important;
            font-size: 14px !important;
        }

        .upload-status-markdown {
            padding: 14px 16px !important;
            border-radius: 16px !important;
            border: 1px solid rgba(96, 165, 250, 0.20) !important;
            background: rgba(37, 99, 235, 0.10) !important;
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.04) !important;
        }

        .upload-status-markdown p {
            margin: 0 !important;
        }

        #upload-view .pending,
        #upload-view .generating,
        #upload-view .progress-text {
            color: #dbeafe !important;
        }

        .upload-info-card {
            margin-top: 0 !important;
        }

        .upload-time-picker-row {
            margin-top: 16px !important;
            gap: 8px !important;
        }

        .upload-time-picker-row > .gr-block {
            min-width: 0 !important;
        }

        .upload-time-dropdown {
            flex: 1 1 0 !important;
            min-width: 0 !important;
            background: transparent !important;
        }

        .upload-time-dropdown .wrap,
        .upload-time-dropdown .gr-input,
        .upload-time-dropdown .gr-box,
        .upload-time-dropdown .gr-form,
        .upload-time-dropdown .gradio-dropdown,
        .upload-time-dropdown .dropdown,
        .upload-time-dropdown input,
        .upload-time-dropdown button {
            border-radius: 12px !important;
        }

        .upload-time-dropdown input,
        .upload-time-dropdown button,
        .upload-time-dropdown .wrap {
            min-height: 48px !important;
            background: rgba(11, 18, 40, 0.9) !important;
            border: 1px solid rgba(148, 163, 184, 0.20) !important;
            color: #f8fafc !important;
            font-size: 15px !important;
            font-weight: 700 !important;
            box-shadow: none !important;
        }

        .upload-time-inline-note {
            margin-top: 10px;
            color: rgba(226, 232, 240, 0.58);
            font-size: 12px;
            line-height: 1.6;
        }

        .upload-analyze-btn {
            width: 100% !important;
            margin-top: 14px !important;
            min-height: 48px !important;
            border-radius: 12px !important;
            background: linear-gradient(90deg, #7c3aed 0%, #6d28d9 100%) !important;
            border: none !important;
            color: #f8fafc !important;
            font-size: 15px !important;
            font-weight: 700 !important;
        }

        .upload-feature-card {
            padding: 20px 20px 18px !important;
        }

        .upload-feature-card h3 {
            margin: 0;
            color: #f8fafc;
            font-size: 18px;
            font-weight: 800;
        }

        .upload-feature-list {
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-top: 16px;
        }

        .upload-feature-item {
            display: flex;
            align-items: flex-start;
            gap: 12px;
            padding: 14px;
            border-radius: 16px;
            background: rgba(10, 18, 40, 0.46);
            border: 1px solid rgba(255, 255, 255, 0.07);
        }

        .upload-feature-icon {
            width: 38px;
            height: 38px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 12px;
            flex-shrink: 0;
            font-size: 15px;
        }

        .upload-feature-icon.tone-emerald {
            background: rgba(16, 185, 129, 0.12);
            border: 1px solid rgba(16, 185, 129, 0.22);
        }

        .upload-feature-icon.tone-amber {
            background: rgba(245, 158, 11, 0.12);
            border: 1px solid rgba(245, 158, 11, 0.22);
        }

        .upload-feature-icon.tone-red {
            background: rgba(239, 68, 68, 0.12);
            border: 1px solid rgba(248, 113, 113, 0.22);
        }

        .upload-feature-copy {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }

        .upload-feature-item strong {
            color: #f8fafc;
            font-size: 15px;
        }

        .upload-feature-item span {
            color: rgba(226, 232, 240, 0.66);
            font-size: 13px;
            line-height: 1.6;
        }

        .upload-tip-card {
            padding: 18px 18px 16px !important;
            border: 1px solid rgba(124, 58, 237, 0.24) !important;
            background: linear-gradient(135deg, rgba(80, 30, 180, 0.16) 0%, rgba(28, 52, 115, 0.22) 100%) !important;
        }

        .upload-tip-title {
            color: #fef3c7;
            font-size: 14px;
            font-weight: 700;
        }

        .upload-tip-list {
            margin: 10px 0 0;
            padding-left: 18px;
            color: rgba(226, 232, 240, 0.72);
            font-size: 12px;
            line-height: 1.8;
        }

        @media (max-width: 1100px) {
            .upload-layout {
                width: min(100%, calc(100vw - 28px)) !important;
                grid-template-columns: 1fr !important;
                gap: 20px !important;
            }
        }

        @media (max-width: 768px) {
            #upload-shell-header,
            .upload-layout {
                width: min(100%, calc(100vw - 24px)) !important;
                padding: 20px 0 88px !important;
            }

            .upload-card-copy h3 {
                font-size: 24px;
            }

            .upload-time-picker-row {
                flex-direction: column !important;
            }
        }
        """
    )
