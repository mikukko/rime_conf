#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def find_invisible_chars():
    """查找词典文件中的空白/不可见字符"""
    
    invisible_chars = []
    
    with open('dicts/wubi86_core.dict.yaml', 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            # 跳过注释和元数据行
            stripped = line.strip()
            if not stripped or stripped.startswith('#') or stripped.startswith('---') or stripped.startswith('...'):
                continue
            
            # 检查是否是词典条目格式
            parts = stripped.split('\t')
            if len(parts) >= 3:
                word = parts[0]
                code = parts[1]
                weight = parts[2]
                
                # 检查第一个字段是否为空白/不可见字符
                if not word:
                    invisible_chars.append((line_num, '空字符串', '', code, weight))
                elif len(word) == 1:
                    char_code = ord(word)
                    char_name = f'U+{char_code:04X}'
                    
                    # 检查各种类型的不可见/特殊字符
                    if char_code < 32:  # 控制字符
                        invisible_chars.append((line_num, '控制字符', char_name, code, weight))
                    elif char_code == 127:  # DEL字符
                        invisible_chars.append((line_num, 'DEL字符', char_name, code, weight))
                    elif char_code == 160:  # 不间断空格
                        invisible_chars.append((line_num, '不间断空格', char_name, code, weight))
                    elif char_code == 0x3000:  # 全角空格
                        invisible_chars.append((line_num, '全角空格', char_name, code, weight))
                    elif 0x2000 <= char_code <= 0x200F:  # 各种空格和格式字符
                        invisible_chars.append((line_num, '特殊空格', char_name, code, weight))
                    elif 0x202A <= char_code <= 0x202E:  # 双向文本控制字符
                        invisible_chars.append((line_num, '双向控制字符', char_name, code, weight))
                    elif char_code in [0xFEFF, 0x200B, 0x200C, 0x200D]:  # 零宽字符
                        invisible_chars.append((line_num, '零宽字符', char_name, code, weight))
                    elif 0xE000 <= char_code <= 0xF8FF:  # 私用区
                        invisible_chars.append((line_num, '私用区字符', char_name, code, weight))
                    elif 0xF900 <= char_code <= 0xFAFF:  # CJK兼容汉字
                        invisible_chars.append((line_num, 'CJK兼容字符', char_name, code, weight))
                    elif char_code >= 0x10000:  # 扩展平面字符
                        invisible_chars.append((line_num, '扩展平面字符', char_name, code, weight))
    
    return invisible_chars

if __name__ == '__main__':
    print("查找空白字符（看不见的字符）...")
    print("=" * 80)
    
    invisible_chars = find_invisible_chars()
    
    if invisible_chars:
        print(f"找到 {len(invisible_chars)} 个空白/不可见字符:")
        print()
        print(f"{'行号':<8} {'类型':<15} {'Unicode':<10} {'编码':<8} {'权重':<6}")
        print("-" * 80)
        
        for line_num, char_type, char_name, code, weight in invisible_chars:
            print(f"{line_num:<8} {char_type:<15} {char_name:<10} {code:<8} {weight:<6}")
    else:
        print("未找到空白/不可见字符")
