import type { PropsWithChildren } from 'react'
import { cn } from '../lib/cn'

export function Card({ children, className }: PropsWithChildren<{ className?: string }>) {
  return <article className={cn('panel', className)}>{children}</article>
}
