import React from 'react';
import * as Icons from 'lucide-react';

interface StatusBadgeProps {
  /** lucide icon 名稱，例如 'Trophy'、'Skull'，之後可以從後端設定檔直接帶 */
  icon: string;
  label: string;
  tone: 'win' | 'loss';
}

/**
 * 歷史紀錄用的狀態徽章。icon 用名稱指定，之後 CMS 要換圖示不用改程式。
 */
const StatusBadge: React.FC<StatusBadgeProps> = ({ icon, label, tone }) => {
  const Icon = (Icons as Record<string, React.ComponentType<{ size?: number }>>)[icon] ?? Icons.Circle;
  return (
    <span
      className={`inline-flex items-center gap-1 text-[10px] font-bold uppercase tracking-wider ${
        tone === 'win' ? 'text-green-400' : 'text-red-400'
      }`}
    >
      <Icon size={12} />
      {label}
    </span>
  );
};

export default StatusBadge;
