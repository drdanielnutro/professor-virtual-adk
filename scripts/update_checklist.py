#!/usr/bin/env python3
"""
Script para gerenciar o checklist.json do projeto Professor Virtual ADK.

Funcionalidades:
- Atualizar status de tarefas e subtarefas
- Gerar relatórios de progresso
- Validar transições de status
- Sincronizar estatísticas
- Sincronizar com arquivos Markdown
"""

import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import sys
import re

# Caminho para o arquivo checklist.json
CHECKLIST_PATH = Path(__file__).parent.parent / "tasks" / "checklist.json"


class ChecklistManager:
    def __init__(self, checklist_path: Path = CHECKLIST_PATH):
        self.checklist_path = checklist_path
        self.data = self._load_checklist()
        
    def _load_checklist(self) -> Dict:
        """Carrega o checklist.json."""
        try:
            with open(self.checklist_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Erro: Arquivo {self.checklist_path} não encontrado!")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON: {e}")
            sys.exit(1)
    
    def _save_checklist(self) -> None:
        """Salva o checklist.json com formatação adequada."""
        self.data['last_updated'] = datetime.now().strftime('%Y-%m-%d')
        self._update_statistics()
        
        with open(self.checklist_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def _update_statistics(self) -> None:
        """Atualiza as estatísticas do checklist."""
        stats = {
            'total_phases': len(self.data['phases']),
            'total_tasks': 0,
            'total_subtasks': 0,
            'completed_subtasks': 0,
            'done_subtasks': 0,  # Adiciona done_subtasks
            'in_progress_subtasks': 0,
            'pending_subtasks': 0,
            'blocked_subtasks': 0,
            'cancelled_subtasks': 0
        }
        
        for phase in self.data['phases']:
            stats['total_tasks'] += len(phase.get('tasks', []))
            for task in phase.get('tasks', []):
                for subtask in task.get('subtasks', []):
                    stats['total_subtasks'] += 1
                    status = subtask.get('status', 'pending')
                    stats[f'{status}_subtasks'] += 1
        
        self.data['statistics'] = stats
    
    def _validate_status_transition(self, current_status: str, new_status: str) -> bool:
        """Valida se a transição de status é permitida."""
        allowed_transitions = self.data['status_transitions']['allowed']
        
        # Se o status atual é o mesmo que o novo, é permitido
        if current_status == new_status:
            return True
        
        # Verifica se a transição está na lista de permitidas
        for transition in allowed_transitions:
            if transition['from'] == current_status and transition['to'] == new_status:
                return True
        
        return False
    
    def update_subtask_status(self, subtask_id: str, new_status: str) -> Tuple[bool, str]:
        """Atualiza o status de uma subtarefa específica."""
        valid_statuses = self.data['status_transitions']['valid_statuses']
        
        if new_status not in valid_statuses:
            return False, f"Status '{new_status}' inválido. Válidos: {', '.join(valid_statuses)}"
        
        # Parse do ID hierárquico (ex: 1.1.1)
        parts = subtask_id.split('.')
        if len(parts) != 3:
            return False, f"ID '{subtask_id}' inválido. Use formato X.Y.Z (ex: 1.1.1)"
        
        phase_id, task_id, subtask_num = parts
        
        # Encontra a fase
        phase = None
        for p in self.data['phases']:
            if p['id'] == phase_id:
                phase = p
                break
        
        if not phase:
            return False, f"Fase '{phase_id}' não encontrada"
        
        # Encontra a tarefa
        task = None
        for t in phase.get('tasks', []):
            if t['id'] == f"{phase_id}.{task_id}":
                task = t
                break
        
        if not task:
            return False, f"Tarefa '{phase_id}.{task_id}' não encontrada"
        
        # Encontra a subtarefa
        subtask = None
        for st in task.get('subtasks', []):
            if st['id'] == subtask_id:
                subtask = st
                break
        
        if not subtask:
            return False, f"Subtarefa '{subtask_id}' não encontrada"
        
        # Valida a transição
        current_status = subtask.get('status', 'pending')
        if not self._validate_status_transition(current_status, new_status):
            return False, f"Transição de '{current_status}' para '{new_status}' não é permitida"
        
        # Atualiza o status e timestamps
        subtask['status'] = new_status
        
        if new_status == 'in_progress' and subtask.get('started_at') is None:
            subtask['started_at'] = datetime.now().isoformat()
        elif new_status == 'done' and subtask.get('completed_at') is None:
            subtask['completed_at'] = datetime.now().isoformat()
        
        # Atualiza status da tarefa e fase se necessário
        self._update_parent_statuses(phase, task)
        
        # Salva as alterações
        self._save_checklist()
        
        # Atualiza o arquivo Markdown se configurado
        if task.get('file'):
            self._update_markdown_file(task['file'], subtask)
        
        return True, f"Status atualizado com sucesso para '{new_status}'"
    
    def _update_markdown_file(self, file_path: str, subtask: Dict) -> None:
        """Atualiza o checkbox no arquivo Markdown correspondente."""
        md_path = self.checklist_path.parent / file_path
        if not md_path.exists():
            print(f"Aviso: Arquivo {md_path} não encontrado")
            return
        
        try:
            with open(md_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Procura a linha com o ID da subtarefa
            pattern = rf'\[{re.escape(subtask["id"])}\]'
            found = False
            updated_lines = []
            
            for i, line in enumerate(lines):
                if re.search(pattern, line):
                    found = True
                    if subtask['status'] == 'done' and '- [ ]' in line:
                        # Marca como concluído
                        new_line = line.replace('- [ ]', '- [x]')
                        # Adiciona timestamp como comentário
                        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        new_line = new_line.rstrip() + f' <!-- Concluído em: {timestamp} -->\n'
                        updated_lines.append(new_line)
                    elif subtask['status'] == 'in_progress' and '- [ ]' in line and '<!--' not in line:
                        # Adiciona indicador de em progresso
                        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        new_line = line.rstrip() + f' <!-- 🔄 Em progresso desde: {timestamp} -->\n'
                        updated_lines.append(new_line)
                    else:
                        updated_lines.append(line)
                else:
                    updated_lines.append(line)
            
            if found:
                # Salva o arquivo atualizado
                with open(md_path, 'w', encoding='utf-8') as f:
                    f.writelines(updated_lines)
                print(f"Arquivo {file_path} atualizado com sucesso")
            else:
                print(f"Aviso: ID {subtask['id']} não encontrado no arquivo {file_path}")
                
        except Exception as e:
            print(f"Aviso: Não foi possível atualizar o arquivo Markdown: {e}")
    
    def _update_parent_statuses(self, phase: Dict, task: Dict) -> None:
        """Atualiza os status da tarefa e fase baseado nas subtarefas."""
        # Atualiza status da tarefa
        subtask_statuses = [st['status'] for st in task.get('subtasks', [])]
        
        if all(status == 'done' for status in subtask_statuses):
            task['status'] = 'done'
            if task.get('completed_at') is None:
                task['completed_at'] = datetime.now().isoformat()
        elif any(status == 'in_progress' for status in subtask_statuses):
            task['status'] = 'in_progress'
            if task.get('started_at') is None:
                task['started_at'] = datetime.now().isoformat()
        elif any(status == 'blocked' for status in subtask_statuses):
            task['status'] = 'blocked'
        
        # Atualiza status da fase
        task_statuses = [t['status'] for t in phase.get('tasks', [])]
        
        if all(status == 'done' for status in task_statuses):
            phase['status'] = 'done'
        elif any(status == 'in_progress' for status in task_statuses):
            phase['status'] = 'in_progress'
        elif any(status == 'blocked' for status in task_statuses):
            phase['status'] = 'blocked'
    
    def generate_report(self) -> str:
        """Gera um relatório de progresso."""
        self._update_statistics()
        stats = self.data['statistics']
        
        report = []
        report.append("=" * 60)
        report.append(f"RELATÓRIO DE PROGRESSO - {self.data['project']}")
        report.append(f"Última atualização: {self.data['last_updated']}")
        report.append("=" * 60)
        report.append("")
        
        # Estatísticas gerais
        report.append("RESUMO GERAL:")
        report.append(f"  Fases: {stats['total_phases']}")
        report.append(f"  Tarefas: {stats['total_tasks']}")
        report.append(f"  Subtarefas: {stats['total_subtasks']}")
        report.append("")
        
        # Progresso
        total = stats['total_subtasks']
        if total > 0:
            completed_pct = (stats.get('done_subtasks', 0) / total) * 100
            in_progress_pct = (stats['in_progress_subtasks'] / total) * 100
            pending_pct = (stats['pending_subtasks'] / total) * 100
            
            report.append("PROGRESSO:")
            report.append(f"  ✅ Concluídas: {stats.get('done_subtasks', 0)} ({completed_pct:.1f}%)")
            report.append(f"  🔄 Em progresso: {stats['in_progress_subtasks']} ({in_progress_pct:.1f}%)")
            report.append(f"  ⏳ Pendentes: {stats['pending_subtasks']} ({pending_pct:.1f}%)")
            
            if stats.get('blocked_subtasks', 0) > 0:
                blocked_pct = (stats['blocked_subtasks'] / total) * 100
                report.append(f"  🚫 Bloqueadas: {stats['blocked_subtasks']} ({blocked_pct:.1f}%)")
        
        report.append("")
        report.append("DETALHAMENTO POR FASE:")
        report.append("-" * 40)
        
        for phase in self.data['phases']:
            status_icon = {
                'pending': '⏳',
                'in_progress': '🔄',
                'done': '✅',
                'blocked': '🚫'
            }.get(phase['status'], '❓')
            
            report.append(f"\n{status_icon} {phase['name']} ({phase['id']})")
            
            if phase.get('tasks'):
                for task in phase['tasks']:
                    task_status_icon = {
                        'pending': '⏳',
                        'in_progress': '🔄',
                        'done': '✅',
                        'blocked': '🚫'
                    }.get(task['status'], '❓')
                    
                    subtasks = task.get('subtasks', [])
                    completed = sum(1 for st in subtasks if st['status'] == 'done')
                    total_subtasks = len(subtasks)
                    
                    report.append(f"  {task_status_icon} {task['name']} ({completed}/{total_subtasks})")
            else:
                report.append("  (Sem tarefas definidas ainda)")
        
        return "\n".join(report)
    
    def list_pending_tasks(self) -> List[Dict]:
        """Lista todas as tarefas pendentes."""
        pending = []
        
        for phase in self.data['phases']:
            for task in phase.get('tasks', []):
                for subtask in task.get('subtasks', []):
                    if subtask['status'] == 'pending':
                        pending.append({
                            'phase_name': phase['name'],
                            'task_name': task['name'],
                            'subtask_id': subtask['id'],
                            'description': subtask['description']
                        })
        
        return pending


def main():
    parser = argparse.ArgumentParser(description='Gerenciador de Checklist do Projeto')
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponíveis')
    
    # Comando: update
    update_parser = subparsers.add_parser('update', help='Atualiza o status de uma subtarefa')
    update_parser.add_argument('subtask_id', help='ID da subtarefa (formato: X.Y.Z, ex: 1.1.1)')
    update_parser.add_argument('status', choices=['pending', 'in_progress', 'done', 'blocked', 'cancelled'],
                             help='Novo status')
    
    # Comando: report
    report_parser = subparsers.add_parser('report', help='Gera relatório de progresso')
    
    # Comando: pending
    pending_parser = subparsers.add_parser('pending', help='Lista tarefas pendentes')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    manager = ChecklistManager()
    
    if args.command == 'update':
        success, message = manager.update_subtask_status(
            args.subtask_id, args.status
        )
        print(message)
        if not success:
            sys.exit(1)
    
    elif args.command == 'report':
        print(manager.generate_report())
    
    elif args.command == 'pending':
        pending_tasks = manager.list_pending_tasks()
        if pending_tasks:
            print("TAREFAS PENDENTES:")
            print("-" * 60)
            for task in pending_tasks:
                print(f"\n[{task['subtask_id']}] {task['description']}")
                print(f"  Fase: {task['phase_name']}")
                print(f"  Tarefa: {task['task_name']}")
        else:
            print("Nenhuma tarefa pendente encontrada!")


if __name__ == '__main__':
    main()