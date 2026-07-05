import { ChangeDetectionStrategy, Component, input, output } from '@angular/core';

export interface UiTabItem {
  id: string;
  label: string;
}

@Component({
  selector: 'app-ui-tabs',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div
      class="flex flex-wrap gap-1 rounded-lg border border-border bg-surface-elevated p-1"
      role="tablist"
    >
      @for (tab of tabs(); track tab.id) {
        <button
          type="button"
          role="tab"
          class="rounded-md px-4 py-2 text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary"
          [class.bg-primary]="activeId() === tab.id"
          [class.text-white]="activeId() === tab.id"
          [class.text-muted-foreground]="activeId() !== tab.id"
          [class.hover:bg-primary/5]="activeId() !== tab.id"
          [attr.aria-selected]="activeId() === tab.id"
          (click)="onSelect(tab.id)"
        >
          {{ tab.label }}
        </button>
      }
    </div>
  `,
})
export class UiTabs {
  readonly tabs = input<UiTabItem[]>([]);
  readonly activeId = input.required<string>();
  readonly tabChange = output<string>();

  protected onSelect(id: string): void {
    if (id !== this.activeId()) {
      this.tabChange.emit(id);
    }
  }
}
