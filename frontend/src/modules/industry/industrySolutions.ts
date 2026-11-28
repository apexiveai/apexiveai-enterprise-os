import {
  Activity, Boxes, Factory, Fuel, Hammer, Hotel, Leaf, Truck, type LucideIcon,
} from 'lucide-react'

export type IndustrySolutionKey =
  | 'construction'
  | 'manufacturing'
  | 'energy'
  | 'trading'
  | 'hotels'
  | 'agro'
  | 'highway'
  | 'logistics'

type FieldDefinition = {
  key: string
  label: string
  type?: 'text' | 'date' | 'number'
}

export type IndustrySolutionProduct = {
  key: IndustrySolutionKey
  label: string
  description: string
  icon: LucideIcon
  titleLabel: string
  fields: FieldDefinition[]
  workflows: string[]
}

export const industrySolutions: IndustrySolutionProduct[] = [
  {
    key: 'construction',
    label: 'Construction AI Project Management Agent',
    description: 'Track site projects, owners, budgets, and target dates in one work queue.',
    icon: Hammer,
    titleLabel: 'Project name',
    fields: [
      { key: 'site', label: 'Project site' },
      { key: 'project_manager', label: 'Project manager' },
      { key: 'target_date', label: 'Target completion', type: 'date' },
      { key: 'budget', label: 'Budget estimate', type: 'number' },
    ],
    workflows: ['Project intake', 'Milestone tracking', 'Budget and date follow-up'],
  },
  {
    key: 'manufacturing',
    label: 'Manufacturing Factory Automation RPA',
    description: 'Register production work orders and follow their line, SKU, quantity, and due date.',
    icon: Factory,
    titleLabel: 'Work order',
    fields: [
      { key: 'production_line', label: 'Production line' },
      { key: 'sku', label: 'SKU / product code' },
      { key: 'quantity', label: 'Planned quantity', type: 'number' },
      { key: 'due_date', label: 'Due date', type: 'date' },
    ],
    workflows: ['Work-order intake', 'Line assignment', 'Completion tracking'],
  },
  {
    key: 'energy',
    label: 'Energy AI Operations & Reporting',
    description: 'Record operational readings and prepare an auditable reporting queue.',
    icon: Fuel,
    titleLabel: 'Operations report',
    fields: [
      { key: 'asset', label: 'Asset / meter' },
      { key: 'site', label: 'Site' },
      { key: 'report_date', label: 'Reading date', type: 'date' },
      { key: 'reading', label: 'Reading value', type: 'number' },
      { key: 'unit', label: 'Unit (e.g. kWh)' },
    ],
    workflows: ['Reading capture', 'Report review', 'Reporting status'],
  },
  {
    key: 'trading',
    label: 'Trading AI Sales Agent',
    description: 'Manage sales opportunities, customers, expected value, and follow-up dates.',
    icon: Boxes,
    titleLabel: 'Sales opportunity',
    fields: [
      { key: 'customer', label: 'Customer' },
      { key: 'product', label: 'Product / commodity' },
      { key: 'opportunity_value', label: 'Opportunity value', type: 'number' },
      { key: 'follow_up_date', label: 'Next follow-up', type: 'date' },
    ],
    workflows: ['Lead intake', 'Opportunity follow-up', 'Sales-stage tracking'],
  },
  {
    key: 'hotels',
    label: 'Hotels AI Reservation Chatbot',
    description: 'Maintain a reservation work queue with guest, room, and stay details.',
    icon: Hotel,
    titleLabel: 'Reservation reference',
    fields: [
      { key: 'guest', label: 'Guest name' },
      { key: 'room_type', label: 'Room type' },
      { key: 'check_in', label: 'Check-in', type: 'date' },
      { key: 'check_out', label: 'Check-out', type: 'date' },
    ],
    workflows: ['Reservation intake', 'Stay detail review', 'Reservation status'],
  },
  {
    key: 'agro',
    label: 'Agro AI Agriculture Operations',
    description: 'Schedule farm operations by field, crop, area, and planned date.',
    icon: Leaf,
    titleLabel: 'Farm operation',
    fields: [
      { key: 'farm', label: 'Farm / field' },
      { key: 'crop', label: 'Crop' },
      { key: 'operation', label: 'Operation (planting, irrigation, harvest)' },
      { key: 'planned_date', label: 'Planned date', type: 'date' },
      { key: 'area', label: 'Area / acreage', type: 'number' },
    ],
    workflows: ['Field-operation planning', 'Work scheduling', 'Completion tracking'],
  },
  {
    key: 'highway',
    label: 'Highway Toll Collection Automation',
    description: 'Track toll shifts and reconcile transaction counts and collected amounts.',
    icon: Activity,
    titleLabel: 'Toll shift report',
    fields: [
      { key: 'station', label: 'Toll station' },
      { key: 'lane', label: 'Lane' },
      { key: 'shift_date', label: 'Shift date', type: 'date' },
      { key: 'transaction_count', label: 'Transaction count', type: 'number' },
      { key: 'collection_amount', label: 'Collection amount', type: 'number' },
    ],
    workflows: ['Shift report intake', 'Collection review', 'Reconciliation follow-up'],
  },
  {
    key: 'logistics',
    label: 'Logistics AI Logistics Agent',
    description: 'Coordinate shipment assignments, routes, customers, and delivery dates.',
    icon: Truck,
    titleLabel: 'Shipment reference',
    fields: [
      { key: 'shipment_ref', label: 'Shipment reference' },
      { key: 'customer', label: 'Customer' },
      { key: 'origin', label: 'Origin' },
      { key: 'destination', label: 'Destination' },
      { key: 'delivery_due', label: 'Delivery due', type: 'date' },
    ],
    workflows: ['Shipment intake', 'Dispatch preparation', 'Delivery tracking'],
  },
]
